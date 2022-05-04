# this module defines language support objects

import subprocess
from pathlib import Path
from enum import Enum, auto

# =============================================== GENERAL ==============================================================


class LanguageLabel(Enum):
    CXX = auto()
    CXX11 = auto()
    CXX14 = auto()
    CXX17 = auto()
    CXX20 = auto()

    PYTHON3 = auto()

    HASKELL2010 = auto()

    JAVA = auto()
    SCALA = auto()


class LanguageLabelHolder:
    def __init__(self, label):
        self.label = label

    def is_super_label_of(self, other_label_holder):
        if self.label == LanguageLabel.CXX:
            return other_label_holder.label in {
                LanguageLabel.CXX,
                LanguageLabel.CXX11,
                LanguageLabel.CXX14,
                LanguageLabel.CXX17,
                LanguageLabel.CXX20,
            }
        else:
            return self.label == other_label_holder.label


class LanguageData(LanguageLabelHolder):
    """Data concerning certain programming language execution"""
    def __init__(self, convert_to_executable_fun, label):
        super().__init__(label)
        self.convert_to_executable = convert_to_executable_fun


class ExecutionAndConversionData:
    """Data concerning certain programming language execution WITH GIVEN PARAMETERS"""
    def __init__(self, language_data, time_limit_seconds, memory_limit_megabytes, conversion_opts=None, command_line_opts=None):
        self.language_data = language_data

        self.time_limit_seconds = time_limit_seconds
        self.memory_limit_megabytes = memory_limit_megabytes

        self.conversion_opts = conversion_opts
        self.command_line_opts = command_line_opts

    def __getattr__(self, item):
        try:
            return getattr(self.language_data, item)
        except AttributeError:
            raise AttributeError('NO MATCHING ATTR IN ExecutionAndConversionData HIERARCHY')

# ================================================= CXX ================================================================


def cxx_arbitrary_std_convert_to_executable(cxx_standard):
    def cxx_fixed_std_convert_to_executable(path_to_src, non_colliding_exec_name, conversion_opts=None):
        conversion_opts = conversion_opts if conversion_opts else []

        conversion = subprocess.run(['g++', '-o', non_colliding_exec_name, f'-std=c++{cxx_standard}']
                                    + conversion_opts
                                    + [path_to_src])
        return conversion.returncode

    return cxx_fixed_std_convert_to_executable


class CXXDataSet:
    @staticmethod
    def __init__(standards_collection):
        CXXDataSet.data_set = set()
        for std in standards_collection:
            attr_name = f'cxx{std}_data'
            setattr(CXXDataSet,
                    attr_name,
                    LanguageData(convert_to_executable_fun=cxx_arbitrary_std_convert_to_executable(std),
                                 label=eval(f'LanguageLabel.CXX{std}')))
            CXXDataSet.data_set.add(getattr(CXXDataSet, attr_name))


cxx_data = CXXDataSet([11, 14, 17, 20])

# =============================================== HASKELL ==============================================================


def haskell_convert_to_executable(path_to_src, non_colliding_exec_name, conversion_opts=None):
    conversion = subprocess.run(['ghc', '-o', non_colliding_exec_name] + conversion_opts + [path_to_src])
    return conversion.returncode


class HaskellDataSet:
    @staticmethod
    def __init__():
        HaskellDataSet.haskell_data = LanguageData(convert_to_executable_fun=haskell_convert_to_executable,
                                                   label=LanguageLabel.HASKELL2010)


haskell_data = HaskellDataSet()

# =============================================== PYTHON3 ==============================================================


def python3_arbitrary_interpreter_convert_to_executable(path_to_interpreter):
    def python3_fixed_interpreter_convert_to_executable(path_to_src, non_colliding_exec_name, conversion_opts=None):
        # add shebang
        shebang = '#!' + str(path_to_interpreter)
        with open(non_colliding_exec_name, 'w') as script:
            subprocess.run(['echo', f'{shebang}\n\n'], stdout=script)
            subprocess.run(['cat', path_to_src], stdout=script)
        subprocess.run(['chmod', '+x', non_colliding_exec_name])
        return 0

    return python3_fixed_interpreter_convert_to_executable


class PythonDataSet:
    @staticmethod
    def __init__(interpreter_path_dict):
        PythonDataSet.data_set = set()
        for interpreter in interpreter_path_dict:
            attr_name = f'{interpreter}_data'
            setattr(PythonDataSet,
                    attr_name,
                    LanguageData(convert_to_executable_fun=python3_arbitrary_interpreter_convert_to_executable(
                        path_to_interpreter=interpreter_path_dict[interpreter]
                    ), label=LanguageLabel.PYTHON3))
            PythonDataSet.data_set.add(getattr(PythonDataSet, attr_name))


python_data = PythonDataSet({'python3': Path('/bin/python3')})

# ============================================ JAVA or SCALA ===========================================================

# TODO
