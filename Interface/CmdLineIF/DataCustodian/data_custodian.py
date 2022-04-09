import json
from abc import ABC, abstractmethod
from enum import Enum, auto


class Mode(Enum):
    PROBLEM = auto
    SUBMISSION = auto


class DataCustodian(ABC):
    @abstractmethod
    def fill_in(self, key, val):
        pass

    @abstractmethod
    def dump_data(self):
        pass

    def __init__(self, mode):
        self.path_to_dump = None
        if mode == Mode.PROBLEM:
            self.create_problem_dump()
        else:
            self.create_submission_dump()

    def create_problem_dump(self):  # todo
        pass

    def create_submission_dump(self):  # todo
        pass


class JsonDataCustodian(DataCustodian):
    def __init__(self, mode):
        super(JsonDataCustodian, self).__init__(mode)
        self.gathered_data = {}

    def fill_in(self, key_sequence, val):
        dictionary = self.gathered_data
        for key in key_sequence[:-1]:
            dictionary = dictionary[key]
        dictionary[key_sequence[-1]] = val

    def dump_data(self):
        with open(self.path_to_dump, 'w') as dump:
            json.dump(self.gathered_data, dump, indent=4)
