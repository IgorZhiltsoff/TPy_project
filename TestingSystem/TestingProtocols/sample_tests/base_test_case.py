import unittest
from testing_protocols import VerdictMessage


class BaseTestCase(unittest.TestCase):
    def run_tests(self, protocol, user_submitted_data_to_expected_verdict: dict):
        for user_submitted_data in user_submitted_data_to_expected_verdict:
            expected_verdict = user_submitted_data_to_expected_verdict[user_submitted_data]
            self.assertEqual(expected_verdict, protocol.check(user_submitted_data=user_submitted_data).msg)

    @staticmethod
    def standard_user_submitted_data_to_expected_verdict_generator(verdicts):
        class ToEval:
            def __init__(self, unevaluated):
                self.unevaluated = unevaluated

            def evaluate(self, scope):
                locals().update(scope)
                return eval(self.unevaluated)

        def gen(prefix=''):
            verdict_to_standard_variable_name = {
                VerdictMessage.AC: f'{prefix}accepted',
                VerdictMessage.WA: f'{prefix}wrong_answer',
                VerdictMessage.CE: f'{prefix}compilation_error',
                VerdictMessage.RE: f'{prefix}runtime_error',
                VerdictMessage.TL: f'{prefix}time_limit',
                VerdictMessage.SKIP: f'{prefix}skipped'
            }

            keys_to_vals = map(
                lambda verdict: f"{verdict_to_standard_variable_name[verdict]}: {verdict}",
                verdicts)

            return ToEval(f'{{ {", ".join(keys_to_vals)} }}')
        return gen
