import unittest
import subprocess
from main import InputOutput, InputCustomChecker, RandomInputCustomChecker


def cpp_convert_to_executable(path_to_src, name, conversion_opts=None):
    conversion_opts = conversion_opts if conversion_opts else []

    subprocess.run(['g++', '-o', name] + conversion_opts + [path_to_src])
    return name


class AnswerVerdictTest(unittest.TestCase):
    def test_in_out(self):
        inout = InputOutput({"sample_inout_tests/1.in": "sample_inout_tests/1.out",
                             "sample_inout_tests/2.in": "sample_inout_tests/2.out",
                             "sample_inout_tests/3.in": "sample_inout_tests/3.out"})
        self.assertEqual('AC', inout.check(convert_to_executable=cpp_convert_to_executable,
                                           path_to_src='correct.cpp',
                                           submission_id=1))
        self.assertEqual('WA', inout.check(convert_to_executable=cpp_convert_to_executable,
                                           path_to_src='wrong.cpp',
                                           submission_id=2))

    def test_in_custom(self):
        in_custom = InputCustomChecker({"sample_in_custom_tests/1.in",
                                        "sample_in_custom_tests/2.in",
                                        "sample_in_custom_tests/3.in"},
                                       'sample_in_custom_tests/custom_checker.out')
        self.assertEqual('AC', in_custom.check(convert_to_executable=cpp_convert_to_executable,
                                               path_to_src='correct.cpp',
                                               submission_id=1))
        self.assertEqual('WA', in_custom.check(convert_to_executable=cpp_convert_to_executable,
                                               path_to_src='wrong.cpp',
                                               submission_id=2))

    def test_rand_custom(self):
        rand_custom = RandomInputCustomChecker(3,
                                               'sample_rand_custom_tests/random_generator.out',
                                               'sample_rand_custom_tests/custom_checker.out')
        self.assertEqual('AC', rand_custom.check(convert_to_executable=cpp_convert_to_executable,
                                                 path_to_src='correct.cpp',
                                                 submission_id=1))
        self.assertEqual('WA', rand_custom.check(convert_to_executable=cpp_convert_to_executable,
                                                 path_to_src='wrong.cpp',
                                                 submission_id=2))


if __name__ == '__main__':
    unittest.main()
