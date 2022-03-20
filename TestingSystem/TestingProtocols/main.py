from abc import ABC, abstractmethod
import subprocess


class TestingProtocol(ABC):
    @abstractmethod
    def check(self, path_to_executable, command_line_opts, submission_id):
        pass

    @staticmethod
    def run_code(path_to_executable, path_to_input_file, path_to_output_file, command_line_opts):
        with open(path_to_input_file, 'r') as input_file:
            with open(path_to_output_file, 'w') as output_file:
                feedback = subprocess.run([path_to_executable, command_line_opts],
                                          stdin=input_file, stdout=output_file)
                if feedback.returncode != 0:
                    return TestingProtocol.return_code_to_error_msg[feedback.returncode]
                return 0

    @staticmethod
    def generate_output_path(submission_id):
        return f"/tmp/{submission_id}.out"  # todo: check for existence

    return_code_to_error_msg = {1: "FAIL"}


class InputOutput(TestingProtocol):
    def __init__(self, input_output_paths_dict):
        self.input_output_paths_dict = input_output_paths_dict

    def check(self, path_to_executable, command_line_opts, submission_id):
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

    def check(self, path_to_executable, command_line_opts, submission_id):
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
    def __init__(self,
                 test_count, path_to_input_generation_executable, path_to_checker_exec):
        self.test_count = test_count
        self.path_to_input_generation_executable = path_to_input_generation_executable
        self.path_to_checker_exec = path_to_checker_exec

    def generate_input(self, submission_id):  # todo: timeout
        input_dir = f'/tmp/{submission_id}_rand'  # todo: check for existence
        subprocess.run(['mkdir', input_dir])

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

    def check(self, path_to_executable, command_line_opts, submission_id):
        random_input_paths_set = self.generate_input(submission_id)
        deterministic_protocol = InputCustomChecker(random_input_paths_set, self.path_to_checker_exec)
        return deterministic_protocol.check(path_to_executable, command_line_opts, submission_id)


class CustomTestingCode(TestingProtocol):
    def __init__(self, path_to_testing_exec):
        self.path_to_testing_exec = path_to_testing_exec

    def check(self, path_to_executable, command_line_opts, submission_id):
        pass
