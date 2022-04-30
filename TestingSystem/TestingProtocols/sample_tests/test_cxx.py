import unittest
from base_test_case import BaseTestCase
from testing_protocols import InputOutput, InputCustomChecker, RandomInputCustomChecker, LimitedWorkSpace, \
    UserSubmittedData
from language_support import cxx_data, LanguageLabel

cxx_language_data_set = cxx_data.data_set
warning_opts = ['-O2', '-Werror', '-Wpedantic']

accepted = UserSubmittedData('accepted.cpp', 1, LanguageLabel.CXX11)
wrong_answer = UserSubmittedData('wrong_answer.cpp', 2, LanguageLabel.CXX14)
compilation_error = UserSubmittedData('compilation_error.cpp', 3, LanguageLabel.CXX17)

user_submitted_data_to_expected_verdict_generator = \
    BaseTestCase.standard_user_submitted_data_to_expected_verdict_generator(
        ['AC', 'WA', 'CE']
    )


class CXXAnswerTest(BaseTestCase):
    def test_in_out(self):
        inout = InputOutput(
            input_output_paths_dict={"inout_tests/1.in": "inout_tests/1.out",
                                     "inout_tests/2.in": "inout_tests/2.out",
                                     "inout_tests/3.in": "inout_tests/3.out"},
            language_data_set=cxx_language_data_set,
            conversion_opts=warning_opts
        )

        user_submitted_data_to_expected_verdict = \
            user_submitted_data_to_expected_verdict_generator().evaluate(globals())
        self.run_tests(
            inout,
            user_submitted_data_to_expected_verdict=user_submitted_data_to_expected_verdict
        )

    def test_in_custom(self):
        in_custom = InputCustomChecker(
            input_paths_set={"in_custom_tests/1.in",
                             "in_custom_tests/2.in",
                             "in_custom_tests/3.in"},
            path_to_checker_exec='in_custom_tests/custom_checker.out',
            language_data_set=cxx_language_data_set,
            conversion_opts=warning_opts
        )

        user_submitted_data_to_expected_verdict = \
            user_submitted_data_to_expected_verdict_generator().evaluate(globals())
        self.run_tests(
            in_custom,
            user_submitted_data_to_expected_verdict=user_submitted_data_to_expected_verdict
        )

    def test_rand_custom(self):
        rand_custom = RandomInputCustomChecker(
            test_count=3,
            path_to_input_generation_exec='rand_custom_tests/random_generator.out',
            path_to_checker_exec='rand_custom_tests/custom_checker.out',
            language_data_set=cxx_language_data_set,
            conversion_opts=warning_opts
        )

        user_submitted_data_to_expected_verdict = \
            user_submitted_data_to_expected_verdict_generator().evaluate(globals())
        self.run_tests(
            rand_custom,
            user_submitted_data_to_expected_verdict=user_submitted_data_to_expected_verdict
        )

    def test_limited_work_space(self):
        limited_work_space = LimitedWorkSpace(
            path_to_header='limited_work_space/header.cpp',
            path_to_footer='limited_work_space/footer.cpp',
            extension='.cpp',
            language_data_set=cxx_language_data_set,
            conversion_opts=warning_opts
        )

        limited_work_space_accepted = UserSubmittedData('limited_work_space/accepted.cpp', 1, LanguageLabel.CXX)
        limited_work_space_wrong_answer = UserSubmittedData('limited_work_space/wrong_answer.cpp', 2, LanguageLabel.CXX)
        limited_work_space_compilation_error = UserSubmittedData('compilation_error.cpp', 2, LanguageLabel.CXX)

        user_submitted_data_to_expected_verdict = \
            user_submitted_data_to_expected_verdict_generator('limited_work_space_').evaluate(locals())
        self.run_tests(
            limited_work_space,
            user_submitted_data_to_expected_verdict=user_submitted_data_to_expected_verdict
        )


if __name__ == '__main__':
    unittest.main()
