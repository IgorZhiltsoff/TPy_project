import os
from abc import ABC, abstractmethod
import subprocess
from pathlib import Path
import tempfile
from enum import Enum, auto
from contextlib import contextmanager
import re
from language_support import LanguageLabelHolder


class UserSubmittedData(LanguageLabelHolder):
    """Submission specific data: source (its location), submission_id
       Full submission data is stored in Submission class,
       which is composed out of UserSubmittedData and ProblemData"""

    def __init__(self, path_to_src, submission_id, label):
        super().__init__(label)
        self.path_to_src = path_to_src
        self.submission_id = submission_id


class VerdictMessage(Enum):
    AC = auto()
    WA = auto()
    CE = auto()
    RE = auto()
    TL = auto()
    ML = auto()
    SKIP = auto()  # indicating attempt to run submission on incompatible protocol (wrong language)
    ABORT = auto()  # indicating failure "on problem's side" - trouble with random input generator or custom checker


class ResourceConsumption:
    def __init__(self, time_elapsed_milliseconds, memory_consumption_kilobytes):
        self.time_elapsed_milliseconds = time_elapsed_milliseconds
        self.memory_consumption_kilobytes = memory_consumption_kilobytes


class Verdict:
    """An object of this type is to be returned upon testing is finished"""

    def __init__(self, msg, test_number, avg_time_elapsed, avg_memory_consumption_kilobytes):
        self.msg = msg
        self.test_number = test_number
        self.avg_time_elapsed = avg_time_elapsed
        self.avg_memory_consumption_kilobytes = avg_memory_consumption_kilobytes

    def __getattr__(self, item):
        if item == 'memory_consumption_megabytes':
            return self.memory_consumption_kilobytes / 1000


class TestingProtocol(ABC):
    """Abstract class for testing protocols - a data type that constitutes
       the process of testing a solution. API includes 3 methods:
           abstract section:
                - check - for running the submission on tests
           static section:
                - run_code - aux method for running submissions
                - generate_output/exec_path - aux for file acquisition
       Aggregated by ProblemData class in relation one problem_data_upload to many protocols

       Most likely combinations:
            - Several protocols for different programming languages
            - RandomInputCustomChecker for stress/performance testing, other protocol to validate extreme cases"""

    def __init__(self, execution_and_conversion_data_set):
        self.execution_and_conversion_data_set = execution_and_conversion_data_set

    def check(self, user_submitted_data):
        language_data = self.choose_language_data(user_submitted_data)
        if language_data is not None:
            return self.check_with_chosen_language_data(user_submitted_data, language_data)
        else:
            return Verdict(
                msg=VerdictMessage.SKIP,
                test_number=-1,
                avg_time_elapsed=0,
                avg_memory_consumption_kilobytes=0
            )

    @abstractmethod
    def check_with_chosen_language_data(self, user_submitted_data, execution_and_conversion_data):
        pass

    def verify(self, scope) -> (int, bool):
        pass

    @staticmethod
    @contextmanager
    def executable_file():
        with tempfile.NamedTemporaryFile() as executable:
            executable.file.close()
            yield executable

    def basic_check_with_chosen_language_data(
            self,
            user_submitted_data,
            execution_and_conversion_data,
            attr_to_iterate_over
    ):
        with TestingProtocol.executable_file() as executable:
            path_to_executable = executable.name

            conversion_return_code = execution_and_conversion_data.convert_to_executable(
                user_submitted_data.path_to_src,
                path_to_executable,
                execution_and_conversion_data.conversion_opts
            )

            if conversion_return_code != 0:
                return Verdict(
                    msg=VerdictMessage.CE,
                    test_number=-1,
                    avg_time_elapsed=0,
                    avg_memory_consumption_kilobytes=0
                )

            with tempfile.NamedTemporaryFile() as solution_output:
                path_to_solution_output = solution_output.name

                avg_time_elapsed = 0
                avg_memory_consumption_kilobytes = 0

                # ITERATE OVER TESTS
                for test, path_to_input_file in enumerate(attr_to_iterate_over):
                    # RUN
                    returnee, resource_consumption = TestingProtocol.run_code(
                        path_to_executable=path_to_executable,
                        path_to_input_file=path_to_input_file,
                        path_to_solution_output=path_to_solution_output,
                        command_line_opts=execution_and_conversion_data.command_line_opts,
                        time_limit_seconds=execution_and_conversion_data.time_limit_seconds,
                        memory_limit_megabytes=execution_and_conversion_data.memory_limit_megabytes
                    )

                    avg_time_elapsed += resource_consumption.time_elapsed_milliseconds
                    avg_memory_consumption_kilobytes += resource_consumption.memory_consumption_kilobytes

                    cur_avg_time_elapsed = avg_time_elapsed / (test + 1)
                    cur_avg_memory_consumption_kilobytes = avg_memory_consumption_kilobytes / (test + 1)
                    if returnee != 0:
                        return TestingProtocol.deduce_negative_verdict(
                            resource_consumption=resource_consumption,
                            time_limit_seconds=execution_and_conversion_data.time_limit_seconds,
                            memory_limit_megabytes=execution_and_conversion_data.memory_limit_megabytes,
                            test_number=test,
                            avg_time_elapsed=cur_avg_time_elapsed,
                            avg_memory_consumption_kilobytes=cur_avg_memory_consumption_kilobytes
                        )

                    # CHECK
                    attempts_left = TestingProtocol.HELPER_ATTEMPTS_LIMIT
                    while attempts_left > 0:
                        verification_returnee, verification_successful = self.verify(locals())
                        if verification_returnee == 0:
                            break
                        attempts_left -= 1

                    if attempts_left == 0:
                        return Verdict(
                                    msg=VerdictMessage.ABORT,
                                    test_number=-1,
                                    avg_time_elapsed=0,
                                    avg_memory_consumption_kilobytes=0
                                )

                    if not verification_successful:
                        return Verdict(
                            msg=VerdictMessage.WA,
                            test_number=test,
                            avg_time_elapsed=cur_avg_time_elapsed,
                            avg_memory_consumption_kilobytes=cur_avg_memory_consumption_kilobytes
                        )

                    test += 1

        avg_time_elapsed /= test
        avg_memory_consumption_kilobytes /= test
        return Verdict(
            msg=VerdictMessage.AC,
            test_number=-1,
            avg_time_elapsed=avg_time_elapsed,
            avg_memory_consumption_kilobytes=avg_memory_consumption_kilobytes
        )

    def choose_language_data(self, user_submitted_data):
        for execution_and_conversion_data in self.execution_and_conversion_data_set:
            if execution_and_conversion_data.is_super_label_of(user_submitted_data):
                return execution_and_conversion_data
        return None

    @staticmethod
    def run_code(path_to_executable, path_to_input_file, path_to_solution_output,
                 command_line_opts,
                 time_limit_seconds, memory_limit_megabytes):
        command_line_opts = command_line_opts if command_line_opts else []

        with open(path_to_input_file, 'r') as input_file:
            with open(path_to_solution_output, 'w+b') as output_file:
                subprocess.run(['sudo', 'chmod', '777', path_to_executable])

                process = subprocess.run(['sudo', '-u', 'nobody',

                                          TestingProtocol.path_to_timeout,
                                          '-t', str(time_limit_seconds),
                                          '-m', str(int(memory_limit_megabytes * 1000)),
                                          '--confess',

                                          path_to_executable] + command_line_opts,
                                         stdin=input_file, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if process.returncode == 0:
                    output_file.write(process.stdout)
                resource_consumption = TestingProtocol.parse_timeout_stderr(stderr_encoded=process.stderr)
                return process.returncode, resource_consumption

    @staticmethod
    def parse_timeout_stderr(stderr_encoded):
        time_pattern = re.compile(r'<time name="ALL">(\d+)</time>')
        memory_pattern = re.compile(r'MEM (\d+)')

        stderr = stderr_encoded.decode()

        try:
            time_elapsed_milliseconds = int(time_pattern.search(stderr).group(1))
        except AttributeError:
            # the process ran too fast for timeout to measure it, thus, it skipped the field, making search return None
            time_elapsed_milliseconds = 0
        memory_consumption_kilobytes = int(memory_pattern.search(stderr).group(1))

        return ResourceConsumption(
            time_elapsed_milliseconds=time_elapsed_milliseconds,
            memory_consumption_kilobytes=memory_consumption_kilobytes
        )

    @staticmethod
    def deduce_negative_verdict(resource_consumption,
                                time_limit_seconds, memory_limit_megabytes,
                                test_number, avg_time_elapsed, avg_memory_consumption_kilobytes):
        if resource_consumption.time_elapsed_milliseconds >= time_limit_seconds * 1000:
            msg = VerdictMessage.TL
        elif resource_consumption.memory_consumption_kilobytes > memory_limit_megabytes * 1000:
            msg = VerdictMessage.ML
        else:
            msg = VerdictMessage.RE

        return Verdict(
            msg=msg,
            test_number=test_number,
            avg_time_elapsed=avg_time_elapsed,
            avg_memory_consumption_kilobytes=avg_memory_consumption_kilobytes
        )

    HELPER_TIME_LIMIT_SECONDS = 8
    HELPER_MEMORY_LIMIT_MEGABYTES = 1024
    HELPER_ATTEMPTS_LIMIT = 20
    path_to_timeout = os.path.relpath(Path(os.path.dirname(__file__)) / '../timeout/timeout')


class InputOutput(TestingProtocol):
    """The simplest testing protocol which runs submission on given input and asserts equality with given output"""

    def __init__(self, input_output_paths_dict, **kwargs):
        super().__init__(**kwargs)
        self.input_output_paths_dict = input_output_paths_dict

    @staticmethod
    def nonempty_lines_without_trailing_whitespaces(file):
        lines = file.readlines()
        return list(map(lambda line: line.rstrip(), filter(lambda line: line, lines)))

    @staticmethod
    def compare_output(path_to_solution_output, path_to_correct_output):
        with open(path_to_solution_output) as solution_output_raw:
            with open(path_to_correct_output) as correct_output_raw:
                solution_output = InputOutput.nonempty_lines_without_trailing_whitespaces(solution_output_raw)
                correct_output = InputOutput.nonempty_lines_without_trailing_whitespaces(correct_output_raw)
                return solution_output == correct_output

    def verify(self, scope) -> (int, bool):
        path_to_solution_output = scope['path_to_solution_output']
        path_to_input_file = scope['path_to_input_file']
        return 0, InputOutput.compare_output(path_to_solution_output, self.input_output_paths_dict[path_to_input_file])

    def check_with_chosen_language_data(self, user_submitted_data, execution_and_conversion_data):
        return self.basic_check_with_chosen_language_data(
            user_submitted_data=user_submitted_data,
            execution_and_conversion_data=execution_and_conversion_data,
            attr_to_iterate_over=self.input_output_paths_dict
        )


class InputCustomChecker(TestingProtocol):
    """Testing protocol which passes given input to submission and then validates the output running custom code
       Might come in handy in problems with multiple answer"""

    def __init__(self, input_paths_set, path_to_checker_exec, make_paths_relative=True, **kwargs):
        super().__init__(**kwargs)

        self.input_paths_set = set(map(os.path.relpath, input_paths_set)) if make_paths_relative else input_paths_set
        self.path_to_checker_exec_rel = os.path.relpath(path_to_checker_exec)

    def run_custom_checker(self, path_to_input_file, path_to_solution_output):
        subprocess.run(['sudo', 'chmod', '777', os.path.dirname(path_to_input_file)])
        subprocess.run(['sudo', 'chmod', '777', path_to_input_file])
        subprocess.run(['sudo', 'chmod', '777', path_to_solution_output])
        subprocess.run(['sudo', 'chmod', '777', self.path_to_checker_exec_rel])

        process = subprocess.run(['sudo', '-u', 'nobody',

                                  TestingProtocol.path_to_timeout,
                                  '-t', str(TestingProtocol.HELPER_TIME_LIMIT_SECONDS),
                                  '-m', str(TestingProtocol.HELPER_MEMORY_LIMIT_MEGABYTES * 1024),
                                  '--confess',

                                  self.path_to_checker_exec_rel, path_to_input_file, path_to_solution_output],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        return process.returncode, process.stdout.decode() == "1"

    def verify(self, scope) -> (int, bool):
        path_to_input_file = scope['path_to_input_file']
        path_to_solution_output = scope['path_to_solution_output']

        return self.run_custom_checker(path_to_input_file, path_to_solution_output)

    def check_with_chosen_language_data(self, user_submitted_data, execution_and_conversion_data):
        return self.basic_check_with_chosen_language_data(
            user_submitted_data=user_submitted_data,
            execution_and_conversion_data=execution_and_conversion_data,
            attr_to_iterate_over=self.input_paths_set
        )


class RandomInputCustomChecker(TestingProtocol):
    """Testing protocol which passes random input to submission and then validates the output running custom code
       Might come in handy in problems in performance or stress tests"""

    def __init__(self, test_count, path_to_input_generation_exec, path_to_checker_exec, **kwargs):
        super().__init__(**kwargs)

        self.test_count = test_count
        self.path_to_input_generation_exec_rel = os.path.relpath(path_to_input_generation_exec)
        self.path_to_checker_exec_rel = os.path.relpath(path_to_checker_exec)
        subprocess.run(['sudo', 'chmod', '777', path_to_input_generation_exec])
        subprocess.run(['sudo', 'chmod', '777', path_to_checker_exec])

    def generate_input(self, path_to_input_dir):
        input_paths_set = set()
        for test in range(self.test_count):
            path_to_storage = path_to_input_dir / f'{test}.in'  # no need to check collision as placed in fresh dir
            path_to_storage.touch()
            with open(path_to_storage, 'w') as storage:
                attempts_left = TestingProtocol.HELPER_ATTEMPTS_LIMIT
                while attempts_left > 0:
                    return_code = self.run_random_input_generator(storage=storage)
                    if return_code == 0:
                        break
                    attempts_left -= 1
                if attempts_left == 0:
                    return None
            input_paths_set.add(path_to_storage)
        return input_paths_set

    def check_with_chosen_language_data(self, user_submitted_data, execution_and_conversion_data):
        with tempfile.TemporaryDirectory() as path_to_input_dir:
            random_input_paths_set = self.generate_input(Path(path_to_input_dir))
            if not random_input_paths_set:
                return Verdict(
                    msg=VerdictMessage.ABORT,
                    test_number=-1,
                    avg_time_elapsed=0,
                    avg_memory_consumption_kilobytes=0
                )

            deterministic_protocol = InputCustomChecker(
                input_paths_set=random_input_paths_set,
                path_to_checker_exec=self.path_to_checker_exec_rel,
                execution_and_conversion_data_set={execution_and_conversion_data},
                make_paths_relative=False
            )

            return deterministic_protocol.check(user_submitted_data=user_submitted_data)

    def run_random_input_generator(self, storage):
        return subprocess.run(['sudo', '-u', 'nobody',

                               TestingProtocol.path_to_timeout,
                               '-t', str(TestingProtocol.HELPER_TIME_LIMIT_SECONDS),
                               '-m', str(TestingProtocol.HELPER_MEMORY_LIMIT_MEGABYTES * 1024),
                               '--confess',

                               self.path_to_input_generation_exec_rel], stdout=storage).returncode


class LimitedWorkSpace(TestingProtocol):
    """Testing protocol which enables validation of student's functions or other parts of code,
       instead of full programmes. The problem_data_upload contributor uploads a header and a footer which
       would be prepended and appended to student's code. Upon execution, this merged code
       should return 1 or 0, indicating whether the submitted implementation is correct"""

    def __init__(self, path_to_header, path_to_footer, extension, **kwargs):
        super().__init__(**kwargs)

        self.path_to_header = path_to_header
        self.path_to_footer = path_to_footer
        self.extension = extension

    @staticmethod
    @contextmanager
    def unit_file():
        with tempfile.NamedTemporaryFile() as unit:
            unit.write("1".encode())
            unit.flush()
            yield unit

    @contextmanager
    def merged_file(self, user_submitted_data):
        with tempfile.NamedTemporaryFile(suffix=self.extension) as merged:
            for path in [self.path_to_header, user_submitted_data.path_to_src, self.path_to_footer]:
                with open(path, 'r+b') as contents:
                    merged.write(contents.read())
                    merged.write(os.linesep.encode())
            merged.flush()
            yield merged

    def check_with_chosen_language_data(self, user_submitted_data, execution_and_conversion_data):
        # GENERATE SRC
        with self.merged_file(user_submitted_data) as merged:
            path_to_merged = merged.name

            # REINTERPRET CUSTOM TESTING AS INPUT-OUTPUT TESTING
            with LimitedWorkSpace.unit_file() as unit:
                path_to_unit = unit.name
                with tempfile.NamedTemporaryFile() as empty:
                    trivial_protocol = InputOutput(
                        input_output_paths_dict={empty.name: path_to_unit},
                        execution_and_conversion_data_set={execution_and_conversion_data},
                    )
                    merged_data = UserSubmittedData(
                        path_to_src=path_to_merged,
                        submission_id=user_submitted_data.submission_id,
                        label=user_submitted_data.label
                    )
                    return trivial_protocol.check(user_submitted_data=merged_data)


class ProblemData:
    """Problem-specific data: problem_data_upload id and testing protocols"""

    def __init__(self, problem_id, testing_protocols_set):
        self.problem_id = problem_id
        self.testing_protocols_set = testing_protocols_set

    def check(self, user_submitted_data):
        for protocol_number, testing_protocol in enumerate(self.testing_protocols_set):
            verdict = testing_protocol.check(user_submitted_data)
            if verdict.msg != VerdictMessage.AC:
                return f'{verdict.msg}{protocol_number}.{verdict.test_number}'
        return VerdictMessage.AC
