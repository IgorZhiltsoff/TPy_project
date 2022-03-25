import unittest
import subprocess
from testing_protocols import InputOutput, InputCustomChecker, RandomInputCustomChecker, LimitedWorkSpace


def cpp_convert_to_executable(path_to_src, name, conversion_opts=None):
    conversion_opts = conversion_opts if conversion_opts else []

    subprocess.run(['g++', '-o', name] + conversion_opts + [path_to_src])
    return name


class AnswerVerdictTest(unittest.TestCase):
    def test_in_out(self):
        inout = InputOutput({"inout_tests/1.in": "inout_tests/1.out",
                             "inout_tests/2.in": "inout_tests/2.out",
                             "inout_tests/3.in": "inout_tests/3.out"})
        self.assertEqual('AC', inout.check(path_to_src='correct.cpp', submission_id=1,
                                           convert_to_executable=cpp_convert_to_executable))
        self.assertEqual('WA', inout.check(path_to_src='wrong.cpp', submission_id=2,
                                           convert_to_executable=cpp_convert_to_executable))

    def test_in_custom(self):
        in_custom = InputCustomChecker({"in_custom_tests/1.in",
                                        "in_custom_tests/2.in",
                                        "in_custom_tests/3.in"},
                                       'in_custom_tests/custom_checker.out')
        self.assertEqual('AC',
                         in_custom.check(path_to_src='correct.cpp', submission_id=3,
                                         convert_to_executable=cpp_convert_to_executable))
        self.assertEqual('WA', in_custom.check(path_to_src='wrong.cpp', submission_id=4,
                                               convert_to_executable=cpp_convert_to_executable))

    def test_rand_custom(self):
        rand_custom = RandomInputCustomChecker(3,
                                               'rand_custom_tests/random_generator.out',
                                               'rand_custom_tests/custom_checker.out')
        self.assertEqual('AC',
                         rand_custom.check(path_to_src='correct.cpp', submission_id=5,
                                           convert_to_executable=cpp_convert_to_executable))
        self.assertEqual('WA',
                         rand_custom.check(path_to_src='wrong.cpp', submission_id=6,
                                           convert_to_executable=cpp_convert_to_executable))

    def test_limited_work_space(self):
        limited_work_space = LimitedWorkSpace(
            header_location='limited_work_space/header.cpp',
            footer_location='limited_work_space/footer.cpp',
            convert_merged_to_executable=cpp_convert_to_executable,
            extension='.cpp'
        )

        self.assertEqual('AC',
                         limited_work_space.check(path_to_src='limited_work_space/correct.cpp', submission_id=7))
        self.assertEqual('WA',
                         limited_work_space.check(path_to_src='limited_work_space/wrong.cpp', submission_id=8))


if __name__ == '__main__':
    unittest.main()
