from abc import ABC, abstractmethod
import subprocess
from pathlib import Path
from random import randint
from language_support import LanguageLabelHolder


class UserSubmittedData(LanguageLabelHolder):
    """Submission specific data: source (its location), submission_id
       Full submission data is stored in Submission class,
       which is composed out of UserSubmittedData and ProblemData"""
    def __init__(self, path_to_src, submission_id, label):
        super().__init__(label)
        self.path_to_src = path_to_src
        self.submission_id = submission_id


class Verdict:
    """An object of this type is to be returned upon testing is finished"""
    def __init__(self, msg, test_number):
        self.msg = msg
        self.test_number = test_number


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

    def __init__(self, language_data_set, conversion_opts=None, command_line_opts=None):
        self.language_data_set = language_data_set
        self.conversion_opts = conversion_opts
        self.command_line_opts = command_line_opts

    def check(self, user_submitted_data):
        language_data = self.choose_language_data(user_submitted_data)
        if language_data is not None:
            return self.check_with_chosen_language_data(user_submitted_data, language_data)
        else:
            return Verdict("SKIP", -1)

    @abstractmethod
    def check_with_chosen_language_data(self, user_submitted_data, language_data):
        pass

    def choose_language_data(self, user_submitted_data):
        for language_data in self.language_data_set:
            if language_data.is_super_label_of(user_submitted_data):
                return language_data
        return None

    @staticmethod
    def run_code(path_to_executable, path_to_input_file, path_to_output_file, command_line_opts):
        command_line_opts = command_line_opts if command_line_opts else []

        with open(path_to_input_file, 'r') as input_file:
            with open(path_to_output_file, 'w') as output_file:
                feedback = subprocess.run([path_to_executable] + command_line_opts,
                                          stdin=input_file, stdout=output_file)
                if feedback.returncode != 0:
                    return TestingProtocol.return_code_to_error_msg[feedback.returncode]
                return 0

    @staticmethod
    def prevent_path_collision(initial_number, get_path):
        current_path = get_path(initial_number)
        current_number = initial_number
        while current_path.exists():
            current_number -= randint(1, 1000)  # goes back not to collide with new submissions
            current_number %= 65536
            current_path = get_path(current_number)
        return current_path

    @staticmethod
    def generate_output_path(submission_id):
        def get_out_path(number):
            return Path(f"/tmp/{number}out")

        return TestingProtocol.prevent_path_collision(submission_id, get_out_path)

    @staticmethod
    def generate_exec_path(submission_id):
        def get_exec_path(number):
            return Path(f"/tmp/{number}exe")

        return TestingProtocol.prevent_path_collision(submission_id, get_exec_path)

    return_code_to_error_msg = {1: "FAIL"}


class InputOutput(TestingProtocol):
    """The simplest testing protocol which runs submission on given input and asserts equality with given output"""

    def __init__(self, input_output_paths_dict, **kwargs):
        super().__init__(**kwargs)
        self.input_output_paths_dict = input_output_paths_dict

        # truncate newlines terminating correct output files
        for path_to_input_file in input_output_paths_dict:
            InputOutput.truncate_terminating_newline_if_necessary(input_output_paths_dict[path_to_input_file])

    @staticmethod
    def truncate_terminating_newline_if_necessary(path_to_file):
        last_character = subprocess.run(['tail', '-c', '1', path_to_file],
                                        stdout=subprocess.PIPE).stdout.decode('utf-8')
        if last_character == '\n':
            subprocess.run(['truncate', '-s', '-1', path_to_file])

    @staticmethod
    def equal_files(path_to_solution_output, path_to_correct_output):
        InputOutput.truncate_terminating_newline_if_necessary(path_to_solution_output)
        return subprocess.run(['cmp', '--silent',
                               path_to_solution_output,
                               path_to_correct_output]).returncode == 0

    def check_with_chosen_language_data(self, user_submitted_data, language_data):
        path_to_executable = TestingProtocol.generate_exec_path(user_submitted_data.submission_id)
        conversion_return_code = language_data.convert_to_executable(
                                    user_submitted_data.path_to_src,
                                    path_to_executable,
                                    self.conversion_opts
        )

        if conversion_return_code != 0:
            return Verdict('CE', -1)

        path_to_solution_output = TestingProtocol.generate_output_path(user_submitted_data.submission_id)

        # ITERATE OVER TESTS
        for test, path_to_input_file in enumerate(self.input_output_paths_dict):
            # RUN
            feedback = TestingProtocol.run_code(path_to_executable, path_to_input_file,
                                                path_to_solution_output, self.command_line_opts)
            if feedback != 0:
                return Verdict('RE', test)

            # CHECK
            if not InputOutput.equal_files(path_to_solution_output, self.input_output_paths_dict[path_to_input_file]):
                return Verdict('WA', test)

            test += 1

        return Verdict('AC', -1)


class InputCustomChecker(TestingProtocol):  # todo: checker safety
    """Testing protocol which passes given input to submission and then validates the output running custom code
       Might come in handy in problems with multiple answer"""

    def __init__(self, input_paths_set, path_to_checker_exec, **kwargs):
        super().__init__(**kwargs)

        self.input_paths_set = input_paths_set
        self.path_to_checker_exec = path_to_checker_exec

    def passes_custom_checker(self, path_to_input_file, path_to_solution_output):
        return int(subprocess.run([self.path_to_checker_exec, path_to_input_file, path_to_solution_output],
                                  stdout=subprocess.PIPE).stdout.decode('utf-8')) == 1

    def check_with_chosen_language_data(self, user_submitted_data, language_data):
        path_to_executable = TestingProtocol.generate_exec_path(user_submitted_data.submission_id)
        conversion_return_code = language_data.convert_to_executable(
                                user_submitted_data.path_to_src,
                                path_to_executable,
                                self.conversion_opts
        )

        if conversion_return_code != 0:
            return Verdict('CE', -1)

        path_to_solution_output = TestingProtocol.generate_output_path(user_submitted_data.submission_id)

        # ITERATE OVER TESTS
        for test, path_to_input_file in enumerate(self.input_paths_set):
            # RUN
            feedback = TestingProtocol.run_code(path_to_executable, path_to_input_file,
                                                path_to_solution_output, self.command_line_opts)
            if feedback != 0:
                return Verdict('RE', test)

            # CHECK
            if not self.passes_custom_checker(path_to_input_file, path_to_solution_output):
                return Verdict('WA', test)

            test += 1

        return Verdict('AC', -1)


class RandomInputCustomChecker(TestingProtocol):
    """Testing protocol which passes random input to submission and then validates the output running custom code
       Might come in handy in problems in performance or stress tests"""

    def __init__(self, test_count, path_to_input_generation_exec, path_to_checker_exec, **kwargs):
        super().__init__(**kwargs)

        self.test_count = test_count
        self.path_to_input_generation_exec = path_to_input_generation_exec
        self.path_to_checker_exec = path_to_checker_exec

    @staticmethod
    def generate_input_dir(submission_id):
        def get_rand_dir_path(number):
            return Path(f"/tmp/{number}rand")

        input_dir = TestingProtocol.prevent_path_collision(submission_id, get_rand_dir_path)
        subprocess.run(['mkdir', input_dir])
        return input_dir

    def generate_input(self, submission_id):  # todo: timeout
        input_dir = RandomInputCustomChecker.generate_input_dir(submission_id)

        input_paths_set = set()
        for test in range(self.test_count):
            infile_path = Path(f'{input_dir}/{test}.in')  # no need to check collision as placed in fresh dir
            subprocess.run(['touch', infile_path])
            with open(infile_path, 'w') as infile:
                return_code = -1
                while return_code != 0:
                    return_code = subprocess.run(self.path_to_input_generation_exec, stdout=infile).returncode
            input_paths_set.add(infile_path)
        return input_paths_set

    def check_with_chosen_language_data(self, user_submitted_data, language_data):
        random_input_paths_set = self.generate_input(user_submitted_data.submission_id)

        deterministic_protocol = InputCustomChecker(
            input_paths_set=random_input_paths_set,
            path_to_checker_exec=self.path_to_checker_exec,
            language_data=language_data,
            conversion_opts=self.conversion_opts,
            command_line_opts=self.command_line_opts
        )

        return deterministic_protocol.check(user_submitted_data=user_submitted_data)


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

    def generate_merged_path(self, submission_id):
        def get_merged_path(number):
            return Path(f"/tmp/{number}merge{self.extension}")

        return TestingProtocol.prevent_path_collision(submission_id, get_merged_path)

    @staticmethod
    def generate_unit_file():
        path_to_unit = Path('/tmp/unit')
        if not path_to_unit.exists():
            with open(path_to_unit, 'w') as unit:
                subprocess.run(['echo', '-n', '1'], stdout=unit)
        return path_to_unit

    def generate_merged(self, user_submitted_data):
        path_to_merged = self.generate_merged_path(user_submitted_data.submission_id)
        with open(path_to_merged, 'w') as merged:
            subprocess.run(['sed', '', self.path_to_header, user_submitted_data.path_to_src, self.path_to_footer],
                           stdout=merged)
        return path_to_merged

    def check_with_chosen_language_data(self, user_submitted_data, language_data):
        # GENERATE SRC
        path_to_merged = self.generate_merged(user_submitted_data)

        # REINTERPRET CUSTOM TESTING AS INPUT-OUTPUT TESTING
        path_to_unit = LimitedWorkSpace.generate_unit_file()
        trivial_protocol = InputOutput(
            input_output_paths_dict={Path('/dev/stdin'): path_to_unit},
            language_data=language_data,
            conversion_opts=self.conversion_opts,
            command_line_opts=self.command_line_opts
        )
        merged_data = UserSubmittedData(path_to_merged, user_submitted_data.submission_id, None)
        return trivial_protocol.check(user_submitted_data=merged_data)


class ProblemData:
    """Problem-specific data: problem_data_upload id and testing protocols"""
    def __init__(self, problem_id, testing_protocols_set):
        self.problem_id = problem_id
        self.testing_protocols_set = testing_protocols_set

    def check(self, user_submitted_data):
        for protocol_number, testing_protocol in enumerate(self.testing_protocols_set):
            verdict = testing_protocol.check(user_submitted_data)
            if verdict.msg != 'AC':
                return f'{verdict.msg}{protocol_number}.{verdict.test_number}'
        return 'AC'


class ExtendedSubmission:
    """Full submission data: composed of UserSubmittedData and ProblemData"""
    def __init__(self, user_submitted_data, problem_data):
        self.user_submitted_data = user_submitted_data
        self.problem_data = problem_data
