import json
from abc import ABC, abstractmethod
from flatdict import FlatDict


class DataCustodian(ABC):
    """A class for keeping data which was input by user
    Exists to prevent the necessity to implement
    adapters in case we choose data interchange formats
    other than Json"""

    @abstractmethod
    def nested_fill_in(self, key, val):
        pass

    @abstractmethod
    def dump_data(self):
        pass

    def fill_in(self, key, val):
        self.nested_fill_in((key, ), val)

    def fill_in_subdata(self, subdata):
        if isinstance(subdata, dict):
            subdata = FlatDict(subdata)
        for key_sequence_str in subdata:
            key_sequence = tuple(key_sequence_str.split(subdata._delimiter))
            self.nested_fill_in(key_sequence, subdata[key_sequence_str])

    def __init__(self, path_to_dump_dir, entity_id):
        self.create_dump(path_to_dump_dir, entity_id)

    def create_dump(self, path_to_dump_dir, entity_id):
        self.path_to_dump = f'{path_to_dump_dir}/{entity_id}.json'


class JsonDataCustodian(DataCustodian):
    """Data custodian which works with .json files
    Most probably the best and the only choice"""

    def __init__(self, path_to_dump_dir, entity_id):
        super(JsonDataCustodian, self).__init__(path_to_dump_dir, entity_id)
        self.gathered_data = FlatDict()

    def nested_fill_in(self, key_sequence, val):
        dictionary = self.gathered_data
        for key in key_sequence[:-1]:
            dictionary = dictionary.setdefault(key, {})
        dictionary[key_sequence[-1]] = val

    def dump_data(self):
        with open(self.path_to_dump, 'w') as dump:
            json.dump(self.gathered_data.as_dict(), dump, indent=4)
