import unittest
from base_test_case import BaseTestCase
from testing_protocols import InputOutput, InputCustomChecker, RandomInputCustomChecker, LimitedWorkSpace, \
    UserSubmittedData, VerdictMessage
from language_support import python_data, LanguageLabel, ExecutionAndConversionData

python_language_data_set = python_data.data_set
python_execution_and_conversion_data_set = {
    ExecutionAndConversionData(language_data=language_data, time_limit=1, memory_limit_megabytes=5)
    for language_data in python_language_data_set
}

accepted = UserSubmittedData('accepted.py', 1, LanguageLabel.PYTHON3)
wrong_answer = UserSubmittedData('wrong_answer.py', 2, LanguageLabel.PYTHON3)
runtime_error = UserSubmittedData('runtime_error.py', 3, LanguageLabel.PYTHON3)

user_submitted_data_to_expected_verdict_generator = \
    BaseTestCase.standard_user_submitted_data_to_expected_verdict_generator(
        [VerdictMessage.AC, VerdictMessage.WA, VerdictMessage.RE]
    )


class Python3AnswerTest(BaseTestCase):
    def test_in_out(self):
        inout = InputOutput(
            input_output_paths_dict={"inout_tests/1.in": "inout_tests/1.out",
                                     "inout_tests/2.in": "inout_tests/2.out",
                                     "inout_tests/3.in": "inout_tests/3.out"},
            execution_and_conversion_data_set=python_execution_and_conversion_data_set
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
            execution_and_conversion_data_set=python_execution_and_conversion_data_set
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
            execution_and_conversion_data_set=python_execution_and_conversion_data_set
        )

        user_submitted_data_to_expected_verdict = \
            user_submitted_data_to_expected_verdict_generator().evaluate(globals())
        self.run_tests(
            rand_custom,
            user_submitted_data_to_expected_verdict=user_submitted_data_to_expected_verdict
        )

    def test_limited_work_space(self):
        limited_work_space = LimitedWorkSpace(
            path_to_header='limited_work_space/header.py',
            path_to_footer='limited_work_space/footer.py',
            extension='.py',
            execution_and_conversion_data_set=python_execution_and_conversion_data_set
        )

        limited_work_space_accepted = UserSubmittedData('limited_work_space/accepted.py', 1, LanguageLabel.PYTHON3)
        limited_work_space_wrong_answer = UserSubmittedData('limited_work_space/wrong_answer.py', 2, LanguageLabel.PYTHON3)
        limited_work_space_runtime_error = runtime_error

        user_submitted_data_to_expected_verdict = \
            user_submitted_data_to_expected_verdict_generator('limited_work_space_').evaluate(locals())
        self.run_tests(
            limited_work_space,
            user_submitted_data_to_expected_verdict=user_submitted_data_to_expected_verdict
        )


if __name__ == '__main__':
    unittest.main()
