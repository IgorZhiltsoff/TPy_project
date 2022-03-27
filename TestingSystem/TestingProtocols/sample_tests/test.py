import unittest
import subprocess
from testing_protocols import InputOutput, InputCustomChecker, RandomInputCustomChecker, LimitedWorkSpace, \
    UserSubmittedData, ProgrammingLanguageData
from language_support import cxx_data


correct = UserSubmittedData('correct.cpp', 1)
wrong = UserSubmittedData('wrong.cpp', 2)


class AnswerVerdictTest(unittest.TestCase):
    def test_in_out(self):
        inout = InputOutput(
            input_output_paths_dict={"inout_tests/1.in": "inout_tests/1.out",
                                     "inout_tests/2.in": "inout_tests/2.out",
                                     "inout_tests/3.in": "inout_tests/3.out"},
            programming_language_data=cxx_data.cxx11_data,
            conversion_opts=['-O2', '-Werror', '-Wpedantic']
        )

        self.assertEqual('AC', inout.check(user_submitted_data=correct).msg)
        self.assertEqual('WA', inout.check(user_submitted_data=wrong).msg)

    def test_in_custom(self):
        in_custom = InputCustomChecker(
            input_paths_set={"in_custom_tests/1.in",
                             "in_custom_tests/2.in",
                             "in_custom_tests/3.in"},
            path_to_checker_exec='in_custom_tests/custom_checker.out',
            programming_language_data=cxx_data.cxx11_data,
            conversion_opts=['-O2', '-Werror', '-Wpedantic']
        )
        self.assertEqual('AC', in_custom.check(user_submitted_data=correct).msg)
        self.assertEqual('WA', in_custom.check(user_submitted_data=wrong).msg)

    def test_rand_custom(self):
        rand_custom = RandomInputCustomChecker(
            test_count=3,
            path_to_input_generation_executable='rand_custom_tests/random_generator.out',
            path_to_checker_exec='rand_custom_tests/custom_checker.out',
            programming_language_data=cxx_data.cxx11_data,
            conversion_opts=['-O2', '-Werror', '-Wpedantic']
        )
        self.assertEqual('AC', rand_custom.check(user_submitted_data=correct).msg)
        self.assertEqual('WA', rand_custom.check(user_submitted_data=wrong).msg)

    def test_limited_work_space(self):
        limited_work_space = LimitedWorkSpace(
            path_to_header='limited_work_space/header.cpp',
            path_to_footer='limited_work_space/footer.cpp',
            extension='.cpp',
            programming_language_data=cxx_data.cxx11_data,
            conversion_opts=['-O2', '-Werror', '-Wpedantic']
        )

        limited_work_space_correct = UserSubmittedData('limited_work_space/correct.cpp', 1)
        limited_work_space_wrong = UserSubmittedData('limited_work_space/wrong.cpp', 1)

        self.assertEqual('AC', limited_work_space.check(user_submitted_data=limited_work_space_correct).msg)
        self.assertEqual('WA', limited_work_space.check(user_submitted_data=limited_work_space_wrong).msg)


if __name__ == '__main__':
    unittest.main()
