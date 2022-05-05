import unittest
from base_test_case import BaseTestCase
from testing_protocols import InputCustomChecker, RandomInputCustomChecker, \
    UserSubmittedData, VerdictMessage
from language_support import python_data, LanguageLabel, ExecutionAndConversionData

python_language_data_set = python_data.data_set
python_execution_and_conversion_data_set = {
    ExecutionAndConversionData(language_data=language_data, time_limit_seconds=0.5, memory_limit_megabytes=64)
    for language_data in python_language_data_set
}

accepted = UserSubmittedData('accepted.py', 1, LanguageLabel.PYTHON3)

user_submitted_data_to_expected_verdict_generator_for_faulty_protocols = \
            BaseTestCase.standard_user_submitted_data_to_expected_verdict_generator(
                [VerdictMessage.ABORT]
            )


class AbortTest(BaseTestCase):
    def test_abort_in_custom_memory_limit(self):
        faulty_in_custom = InputCustomChecker(
            input_paths_set={"in_custom_tests/1.in",
                             "in_custom_tests/2.in",
                             "in_custom_tests/3.in"},
            path_to_checker_exec='in_custom_tests/memory_leak_checker.out',
            execution_and_conversion_data_set=python_execution_and_conversion_data_set
        )

        aborted = UserSubmittedData('accepted.py', 1, LanguageLabel.PYTHON3)

        user_submitted_data_to_expected_verdict = \
            user_submitted_data_to_expected_verdict_generator_for_faulty_protocols().evaluate(locals())

        with BaseTestCase.mock_testing_protocol(helper_memory_limit_megabytes=16, helper_attempts_limit=2):
            self.run_tests(
                faulty_in_custom,
                user_submitted_data_to_expected_verdict=user_submitted_data_to_expected_verdict
            )

    def test_abort_rand_custom_time_limit(self):
        faulty_rand_custom = RandomInputCustomChecker(
            test_count=3,
            path_to_input_generation_exec='rand_custom_tests/time_limit_generator.out',
            path_to_checker_exec='rand_custom_tests/custom_checker.out',
            execution_and_conversion_data_set=python_execution_and_conversion_data_set
        )

        aborted = UserSubmittedData('accepted.py', 1, LanguageLabel.PYTHON3)

        user_submitted_data_to_expected_verdict = \
            user_submitted_data_to_expected_verdict_generator_for_faulty_protocols().evaluate(locals())

        with BaseTestCase.mock_testing_protocol(helper_time_limit_seconds=0.1, helper_attempts_limit=2):
            self.run_tests(
                faulty_rand_custom,
                user_submitted_data_to_expected_verdict=user_submitted_data_to_expected_verdict
            )


if __name__ == '__main__':
    unittest.main()
