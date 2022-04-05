import unittest


class TemplateTest(unittest.TestCase):
    def run_tests(self, protocol, user_submitted_data_to_expected_verdict: dict):
        for user_submitted_data, expected_verdict in user_submitted_data_to_expected_verdict:
            self.assertEqual(expected_verdict, protocol.check(user_submitted_data=user_submitted_data).msg)