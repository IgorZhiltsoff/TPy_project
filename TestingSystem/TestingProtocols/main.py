from abc import ABC, abstractmethod
import subprocess


class TestingProtocol(ABC):
    @abstractmethod
    def check(self, path_to_src, submission_id, convert_to_executable=None, conversion_opts=None,
              command_line_opts=None):
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
    def __init__(self, input_output_paths_dict):
        self.input_output_paths_dict = input_output_paths_dict

    def check(self, path_to_src, submission_id, convert_to_executable=None, conversion_opts=None,
              command_line_opts=None):
        path_to_executable = convert_to_executable(path_to_src,
                                                   TestingProtocol.generate_exec_path(submission_id),
                                                   conversion_opts)

        solution_output_location = TestingProtocol.generate_output_path(submission_id)

        # ITERATE OVER TESTS
        for path_to_input_file in self.input_output_paths_dict:
            # RUN
            feedback = TestingProtocol.run_code(path_to_executable, path_to_input_file,
                                                solution_output_location, command_line_opts)
            if feedback != 0:
                return feedback

            # CHECK
            if subprocess.run(['cmp', '--silent', solution_output_location,
                               self.input_output_paths_dict[path_to_input_file]]).returncode != 0:
                return 'WA'

        return 'AC'


class InputCustomChecker(TestingProtocol):  # todo: checker safety
    def __init__(self, input_paths_set, path_to_checker_exec):
        self.input_paths_set = input_paths_set
        self.path_to_checker_exec = path_to_checker_exec

    def check(self, path_to_src, submission_id, convert_to_executable=None, conversion_opts=None,
              command_line_opts=None):
        path_to_executable = convert_to_executable(path_to_src,
                                                   TestingProtocol.generate_exec_path(submission_id),
                                                   conversion_opts)

        solution_output_location = TestingProtocol.generate_output_path(submission_id)

        # ITERATE OVER TESTS
        for path_to_input_file in self.input_paths_set:
            # RUN
            feedback = TestingProtocol.run_code(path_to_executable, path_to_input_file,
                                                solution_output_location, command_line_opts)
            if feedback != 0:
                return feedback

            # CHECK
            if subprocess.run([self.path_to_checker_exec, path_to_input_file, solution_output_location],
                              stdout=subprocess.PIPE).stdout.decode('utf-8') != '1':
                return 'WA'

        return 'AC'


class RandomInputCustomChecker(TestingProtocol):
    def __init__(self, test_count, path_to_input_generation_executable, path_to_checker_exec):
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

    def check(self, path_to_src, submission_id, convert_to_executable=None, conversion_opts=None,
              command_line_opts=None):
        random_input_paths_set = self.generate_input(submission_id)
        deterministic_protocol = InputCustomChecker(random_input_paths_set, self.path_to_checker_exec)
        return deterministic_protocol.check(path_to_src=path_to_src,
                                            submission_id=submission_id,
                                            convert_to_executable=convert_to_executable,
                                            conversion_opts=conversion_opts,
                                            command_line_opts=command_line_opts)


class LimitedWorkSpace(TestingProtocol):
    def __init__(self, header_location, footer_location,
                 convert_merged_to_executable, extension, merged_conversion_opts=None):
        self.header_location = header_location
        self.footer_location = footer_location
        self.convert_merged_to_executable = convert_merged_to_executable
        self.extension = extension
        self.merged_conversion_opts = merged_conversion_opts

    def generate_merged_path(self, submission_id):  # todo: check for existence
        return f"/tmp/{submission_id}merge{self.extension}"

    @staticmethod
    def generate_unit_file():  # todo: check for existence
        unit_location = '/tmp/unit'
        with open(unit_location, 'w') as unit:
            subprocess.run(['echo', '-n', '1'], stdout=unit)
        return unit_location

    def generate_merged(self, path_to_src, submission_id):
        merged_location = self.generate_merged_path(submission_id)
        with open(merged_location, 'w') as merged:
            subprocess.run(['sed', '', self.header_location, path_to_src, self.footer_location], stdout=merged)
        return merged_location

    def check(self, path_to_src, submission_id, convert_to_executable=None, conversion_opts=None,
              command_line_opts=None):
        # GENERATE SRC
        merged_location = self.generate_merged(path_to_src, submission_id)

        # REINTERPRET CUSTOM TESTING AS INPUT-OUTPUT TESTING
        unit_location = LimitedWorkSpace.generate_unit_file()
        trivial_protocol = InputOutput({'/dev/stdin': unit_location})
        return trivial_protocol.check(path_to_src=merged_location,
                                      submission_id=submission_id,
                                      convert_to_executable=self.convert_merged_to_executable,
                                      conversion_opts=self.merged_conversion_opts,
                                      command_line_opts=command_line_opts)
