import unittest


class BaseTestCase(unittest.TestCase):
    def run_tests(self, protocol, user_submitted_data_to_expected_verdict: dict):
        for user_submitted_data in user_submitted_data_to_expected_verdict:
            expected_verdict = user_submitted_data_to_expected_verdict[user_submitted_data]
            self.assertEqual(expected_verdict, protocol.check(user_submitted_data=user_submitted_data).msg)

    def generate_user_submitted_data_to_expected_verdict(self):
        pass
