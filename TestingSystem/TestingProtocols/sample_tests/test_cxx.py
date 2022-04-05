import unittest
from template_test import BaseTestCase
from testing_protocols import InputOutput, InputCustomChecker, RandomInputCustomChecker, LimitedWorkSpace, \
    UserSubmittedData
from language_support import cxx_data


accepted = UserSubmittedData('accepted.cpp', 1)
wrong_answer = UserSubmittedData('wrong_answer.cpp', 2)
compilation_error = UserSubmittedData('compilation_error.cpp', 3)


class CXXAnswerTest(BaseTestCase):
    def test_in_out(self):
        inout = InputOutput(
            input_output_paths_dict={"inout_tests/1.in": "inout_tests/1.out",
                                     "inout_tests/2.in": "inout_tests/2.out",
                                     "inout_tests/3.in": "inout_tests/3.out"},
            programming_language_data=cxx_data.cxx11_data,
            conversion_opts=['-O2', '-Werror', '-Wpedantic']
        )

        self.run_tests(
            inout,
            user_submitted_data_to_expected_verdict={accepted: 'AC',
                                                     wrong_answer: 'WA',
                                                     compilation_error: 'CE'}
        )

    def test_in_custom(self):
        in_custom = InputCustomChecker(
            input_paths_set={"in_custom_tests/1.in",
                             "in_custom_tests/2.in",
                             "in_custom_tests/3.in"},
            path_to_checker_exec='in_custom_tests/custom_checker.out',
            programming_language_data=cxx_data.cxx14_data,
            conversion_opts=['-O2', '-Werror', '-Wpedantic']
        )
        self.run_tests(
            in_custom,
            user_submitted_data_to_expected_verdict={accepted: 'AC',
                                                     wrong_answer: 'WA',
                                                     compilation_error: 'CE'}
        )

    def test_rand_custom(self):
        rand_custom = RandomInputCustomChecker(
            test_count=3,
            path_to_input_generation_executable='rand_custom_tests/random_generator.out',
            path_to_checker_exec='rand_custom_tests/custom_checker.out',
            programming_language_data=cxx_data.cxx17_data,
            conversion_opts=['-O2', '-Werror', '-Wpedantic']
        )
        self.run_tests(
            rand_custom,
            user_submitted_data_to_expected_verdict={accepted: 'AC',
                                                     wrong_answer: 'WA',
                                                     compilation_error: 'CE'}
        )

    def test_limited_work_space(self):
        limited_work_space = LimitedWorkSpace(
            path_to_header='limited_work_space/header.cpp',
            path_to_footer='limited_work_space/footer.cpp',
            extension='.cpp',
            programming_language_data=cxx_data.cxx20_data,
            conversion_opts=['-O2', '-Werror', '-Wpedantic']
        )

        limited_work_space_accepted = UserSubmittedData('limited_work_space/accepted.cpp', 1)
        limited_work_space_wrong_answer = UserSubmittedData('limited_work_space/wrong_answer.cpp', 2)
        limited_work_space_compilation_error = UserSubmittedData('compilation_error.cpp', 2)

        self.run_tests(
            limited_work_space,
            user_submitted_data_to_expected_verdict={limited_work_space_accepted: 'AC',
                                                     limited_work_space_wrong_answer: 'WA',
                                                     limited_work_space_compilation_error: 'CE'}
        )


if __name__ == '__main__':
    unittest.main()
