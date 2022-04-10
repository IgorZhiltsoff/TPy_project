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

    def extend(self, subdata):
        if isinstance(subdata, dict):
            subdata = FlatDict(subdata)
        for key_sequence_str in subdata:
            key_sequence = tuple(key_sequence_str.split(subdata._delimiter))
            item = self.nested_get_item(key_sequence)
            if isinstance(item, list):
                if isinstance(subdata[key_sequence_str], list):
                    item += subdata[key_sequence_str]
                else:
                    item.append(subdata[key_sequence_str])
            else:
                self.nested_fill_in(key_sequence, subdata[key_sequence_str])

    def __init__(self, path_to_dump_dir, entity_id):
        self.path_to_dump = self.create_path_to_dump(path_to_dump_dir, entity_id)

    @staticmethod
    def create_path_to_dump(path_to_dump_dir, entity_id):
        return f'{path_to_dump_dir}/{entity_id}.json'


class JsonDataCustodian(DataCustodian):
    """Data custodian which works with .json files
    Most probably the best and the only choice"""

    def __init__(self, path_to_dump_dir, entity_id):
        super(JsonDataCustodian, self).__init__(path_to_dump_dir, entity_id)
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
        dictionary[key_sequence[-1]].append(val)

    def dump_data(self):
        with open(self.path_to_dump, 'w') as dump:
            json.dump(self.gathered_data.as_dict(), dump, indent=4)
