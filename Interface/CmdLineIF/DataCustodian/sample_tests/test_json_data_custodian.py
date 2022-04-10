import json
import unittest
from data_custodian import JsonDataCustodian


class JsonDataCustodianTest(unittest.TestCase):
    def setUp(self) -> None:
        path_to_dump_dir = '/tmp'
        self.custodian = JsonDataCustodian(path_to_dump_dir, 1)

    def test_fill(self):
        self.custodian.fill_in('1', 'hello')
        self.custodian.fill_in('2', ['bye bye', 'good bye'])
        self.custodian.fill_in('3', {'hi': 10})
        self.custodian.nested_fill_in(('3', '2', 'name'), 'data')
        self.custodian.nested_fill_in(('name', ), 42)
        self.custodian.nested_fill_in(('4', 'name', '1'), 'hello')

        self.custodian.extend(
            {
                '2': ''
                '3': {
                      '2': {'data': 'name'},
                      'hello': 'hi'
                },
                '5': 42
             }
        )

        self.custodian.dump_data()

        input_data = {
            '1': 'hello',
            '2': ['bye bye', 'good bye'],
            '3': {
                  'hi': 10,
                  '2': {
                      'name': 'data',
                      'data': 'name'
                  },
                 'hello': 'hi'
              },
            'name': 42,
            '4': {
                'name': {
                    '1': 'hello'
                }
            },
            '5': 42
        }

        with open(self.custodian.path_to_dump) as dump:
            dumped_data = json.load(dump)
        self.assertEqual(input_data, dumped_data)

    def test_append(self):
        self.custodian.fill_in('1', 'hello')
        self.custodian.fill_in('2', ['bye bye', 'good bye'])
        self.custodian.fill_in('3', {'hi': []})

        self.custodian.append('2', 'hello')
        self.custodian.append('2', 'hi')

        self.custodian.nested_append(('3', 'hi'), 100)
        self.custodian.nested_append(('4', 'data'), 'name')
        self.custodian.nested_append(('4', 'data'), 'info')

        self.


if __name__ == '__main__':
    unittest.main()
