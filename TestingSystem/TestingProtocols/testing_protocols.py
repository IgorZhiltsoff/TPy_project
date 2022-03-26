from abc import ABC, abstractmethod
import subprocess


class UserSubmittedData:
    """Submission specific data: source (its location), submission_id
       Full submission data is stored in Submission class,
       which is composed out of UserSubmittedData and ProblemData"""
    def __init__(self, path_to_src, submission_id):
        self.path_to_src = path_to_src
        self.submission_id = submission_id


class Verdict:
    """An object of this type is to be returned upon testing is finished"""
    def __init__(self, msg, test_number):
        self.msg = msg
        self.test_number = test_number


class ProgrammingLanguageData:
    def __init__(self, convert_to_executable_fun):
        self.convert_to_executable = convert_to_executable_fun


class TestingProtocol(ABC):
    """Abstract class for testing protocols - a data type that constitutes
       the process of testing a solution. API includes 3 methods:
           abstract section:
                - check - for running the submission on tests
           static section:
                - run_code - aux method for running submissions
                - generate_output/exec_path - aux for file acquisition
       Aggregated by ProblemData class in relation one problem to many protocols

       Most likely combinations:
            - Several protocols for different programming languages
            - RandomInputCustomChecker for stress/performance testing, other protocol to validate extreme cases"""

    def __init__(self, convert_to_executable, conversion_opts=None, command_line_opts=None):
        self.convert_to_executable = convert_to_executable
        self.conversion_opts = conversion_opts
        self.command_line_opts = command_line_opts

    @abstractmethod
    def check(self, user_submitted_data):
        pass

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
    def generate_output_path(submission_id):
        return f"/tmp/{submission_id}out"  # todo: check for existence

    @staticmethod
    def generate_exec_path(submission_id):
        return f"/tmp/{submission_id}exe"  # todo: check for existence

    return_code_to_error_msg = {1: "FAIL"}


class InputOutput(TestingProtocol):
    """The simplest testing protocol which runs submission on given input and asserts equality with given output"""

    def __init__(self, input_output_paths_dict,
                 convert_to_executable, conversion_opts=None, command_line_opts=None):
        super().__init__(convert_to_executable, conversion_opts, command_line_opts)
        self.input_output_paths_dict = input_output_paths_dict

    def check(self, user_submitted_data):
        path_to_executable = self.convert_to_executable(
                                user_submitted_data.path_to_src,
                                TestingProtocol.generate_exec_path(user_submitted_data.submission_id),
                                self.conversion_opts
        )

        solution_output_location = TestingProtocol.generate_output_path(user_submitted_data.submission_id)

        # ITERATE OVER TESTS
        test = 0
        for path_to_input_file in self.input_output_paths_dict:
            # RUN
            feedback = TestingProtocol.run_code(path_to_executable, path_to_input_file,
                                                solution_output_location, self.command_line_opts)
            if feedback != 0:
                return feedback

            # CHECK
            if subprocess.run(['cmp', '--silent', solution_output_location,
                               self.input_output_paths_dict[path_to_input_file]]).returncode != 0:
                return Verdict('WA', test)

            test += 1

        return Verdict('AC', -1)


class InputCustomChecker(TestingProtocol):  # todo: checker safety
    """Testing protocol which passes given input to submission and then validates the output running custom code
       Might come in handy in problems with multiple answer"""

    def __init__(self, input_paths_set, path_to_checker_exec,
                 convert_to_executable, conversion_opts=None, command_line_opts=None):
        super().__init__(convert_to_executable, conversion_opts, command_line_opts)

        self.input_paths_set = input_paths_set
        self.path_to_checker_exec = path_to_checker_exec

    def check(self, user_submitted_data):
        path_to_executable = self.convert_to_executable(
                                user_submitted_data.path_to_src,
                                TestingProtocol.generate_exec_path(user_submitted_data.submission_id),
                                self.conversion_opts
        )

        solution_output_location = TestingProtocol.generate_output_path(user_submitted_data.submission_id)

        # ITERATE OVER TESTS
        test = 0
        for path_to_input_file in self.input_paths_set:
            # RUN
            feedback = TestingProtocol.run_code(path_to_executable, path_to_input_file,
                                                solution_output_location, self.command_line_opts)
            if feedback != 0:
                return feedback

            # CHECK
            if subprocess.run([self.path_to_checker_exec, path_to_input_file, solution_output_location],
                              stdout=subprocess.PIPE).stdout.decode('utf-8') != '1':
                return Verdict('WA', test)

            test += 1

        return Verdict('AC', -1)


class RandomInputCustomChecker(TestingProtocol):
    """Testing protocol which passes random input to submission and then validates the output running custom code
       Might come in handy in problems in performance or stress tests"""

    def __init__(self, test_count, path_to_input_generation_executable, path_to_checker_exec,
                 convert_to_executable, conversion_opts=None, command_line_opts=None):
        super().__init__(convert_to_executable, conversion_opts, command_line_opts)

        self.test_count = test_count
        self.path_to_input_generation_executable = path_to_input_generation_executable
        self.path_to_checker_exec = path_to_checker_exec

    @staticmethod
    def generate_input_dir(submission_id):  # todo: check for existence
        input_dir = f'/tmp/{submission_id}rand'
        subprocess.run(['mkdir', input_dir])
        return input_dir

    def generate_input(self, submission_id):  # todo: timeout
        input_dir = RandomInputCustomChecker.generate_input_dir(submission_id)

        input_paths_set = set()
        for test in range(self.test_count):
            infile_path = f'{input_dir}/{test}.in'
            subprocess.run(['touch', infile_path])
            with open(infile_path, 'w') as infile:
                return_code = -1
                while return_code != 0:
                    return_code = subprocess.run(self.path_to_input_generation_executable, stdout=infile).returncode
            input_paths_set.add(infile_path)
        return input_paths_set

    def check(self, user_submitted_data):
        random_input_paths_set = self.generate_input(user_submitted_data.submission_id)

        deterministic_protocol = InputCustomChecker(
            input_paths_set=random_input_paths_set,
            path_to_checker_exec=self.path_to_checker_exec,
            convert_to_executable=self.convert_to_executable,
            conversion_opts=self.conversion_opts,
            command_line_opts=self.command_line_opts
        )

        return deterministic_protocol.check(user_submitted_data=user_submitted_data)


class LimitedWorkSpace(TestingProtocol):
    """Testing protocol which enables validation of student's functions or other parts of code,
       instead of full programmes. The problem contributor uploads a header and a footer which
       would be prepended and appended to student's code. Upon execution, this merged code
       should return 1 or 0, indicating whether the submitted implementation is correct"""

    def __init__(self, header_location, footer_location, extension,
                 convert_to_executable, conversion_opts=None, command_line_opts=None):
        super().__init__(convert_to_executable, conversion_opts, command_line_opts)

        self.header_location = header_location
        self.footer_location = footer_location
        self.extension = extension

    def generate_merged_path(self, submission_id):  # todo: check for existence
        return f"/tmp/{submission_id}merge{self.extension}"

    @staticmethod
    def generate_unit_file():  # todo: check for existence
        unit_location = '/tmp/unit'
        with open(unit_location, 'w') as unit:
            subprocess.run(['echo', '-n', '1'], stdout=unit)
        return unit_location

    def generate_merged(self, user_submitted_data):
        merged_location = self.generate_merged_path(user_submitted_data.submission_id)
        with open(merged_location, 'w') as merged:
            subprocess.run(['sed', '', self.header_location, user_submitted_data.path_to_src, self.footer_location],
                           stdout=merged)
        return merged_location

    def check(self, user_submitted_data):
        # GENERATE SRC
        merged_location = self.generate_merged(user_submitted_data)

        # REINTERPRET CUSTOM TESTING AS INPUT-OUTPUT TESTING
        unit_location = LimitedWorkSpace.generate_unit_file()
        trivial_protocol = InputOutput(
            input_output_paths_dict={'/dev/stdin': unit_location},
            convert_to_executable=self.convert_to_executable,
            conversion_opts=self.conversion_opts,
            command_line_opts=self.command_line_opts
        )
        merged_data = UserSubmittedData(merged_location, user_submitted_data.submission_id)
        return trivial_protocol.check(user_submitted_data=merged_data)


class ProblemData:
    """Problem-specific data: problem id and testing protocols"""
    def __init__(self, problem_id, testing_protocols_set):
        self.problem_id = problem_id
        self.testing_protocols_set = testing_protocols_set


class ExtendedSubmission:
    """Full submission data: composed of UserSubmittedData and ProblemData"""
    def __init__(self, user_submitted_data, problem_data):
        self.user_submitted_data = user_submitted_data
        self.problem_data = problem_data
