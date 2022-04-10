import json
from abc import ABC, abstractmethod
from flatdict import FlatDict


class DataCustodian(ABC):
    """A class for keeping data which was input by user
    Exists to prevent the necessity to implement
    adapters in case we choose data interchange formats
    other than Json"""

    @abstractmethod
    def nested_get_item(self, key_sequence):
        pass

    @abstractmethod
    def nested_fill_in(self, key_sequence, val):
        pass

    @abstractmethod
    def nested_append(self, key_sequence, val):
        pass

    @abstractmethod
    def dump_data(self):
        pass

    def fill_in(self, key, val):
        self.nested_fill_in((key, ), val)

    def append(self, key, val):
        self.nested_append((key, ), val)

    def get_item(self, key):
        self.nested_get_item((key,))

    def __init__(self, path_to_dump_dir, entity_name):
        self.path_to_dump = self.create_path_to_dump(path_to_dump_dir, entity_name)

    def get_list_reference(self, key_sequence):  # just an alias for get_item, directly saying we are getting a list
        return self.nested_get_item(key_sequence)

    @staticmethod
    def create_path_to_dump(path_to_dump_dir, entity_name):
        return f'{path_to_dump_dir}/{entity_name}.json'


class JsonDataCustodian(DataCustodian):
    """Data custodian which works with .json files
    Most probably the best and the only choice"""

    def __init__(self, path_to_dump_dir, entity_name):
        super(JsonDataCustodian, self).__init__(path_to_dump_dir, entity_name)
        self.gathered_data = FlatDict()

    def nested_get_item(self, key_sequence):
        val = self.gathered_data
        for key in key_sequence:
            val = val.setdefault(key, {})
        return val

    def nested_fill_in(self, key_sequence, val):
        dictionary = self.nested_get_item(key_sequence[:-1])
        dictionary[key_sequence[-1]] = val

    def nested_append(self, key_sequence, val):
        dictionary = self.nested_get_item(key_sequence[:-1])
        dictionary.setdefault(key_sequence[-1], []).append(val)

    def dump_data(self):
        with open(self.path_to_dump, 'w') as dump:
            json.dump(self.gathered_data.as_dict(), dump, indent=4)
