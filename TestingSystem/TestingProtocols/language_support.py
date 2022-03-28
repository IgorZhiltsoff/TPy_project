# this module defines language support objects

from testing_protocols import ProgrammingLanguageData
import subprocess
from pathlib import Path


# ================================================= CXX ================================================================


def cxx_arbitrary_std_convert_to_executable(cxx_standard):
    def cxx_fixed_std_convert_to_executable(path_to_src, non_colliding_exec_name, conversion_opts=None):
        conversion_opts = conversion_opts if conversion_opts else []

        conversion = subprocess.run(['g++', '-o', non_colliding_exec_name, f'-std=c++{cxx_standard}']
                                    + conversion_opts
                                    + [path_to_src])
        return conversion.returncode

    return cxx_fixed_std_convert_to_executable


class CXXData:
    @staticmethod
    def __init__(standards_collection):
        for std in standards_collection:
            setattr(CXXData,
                    f'cxx{std}_data',
                    ProgrammingLanguageData(
                        convert_to_executable_fun=cxx_arbitrary_std_convert_to_executable(std)
                    ))


cxx_data = CXXData([11, 14, 17, 20])

# =============================================== HASKELL ==============================================================


def haskell_convert_to_executable(path_to_src, non_colliding_exec_name, conversion_opts=None):
    conversion = subprocess.run(['ghc', '-o', non_colliding_exec_name] + conversion_opts + [path_to_src])
    return conversion.returncode


class HaskellData:
    @staticmethod
    def __init__():
        HaskellData.haskell_data = ProgrammingLanguageData(
                        convert_to_executable_fun=haskell_convert_to_executable
                    )


haskell_data = HaskellData()

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


class PythonData:
    @staticmethod
    def __init__(interpreter_path_dict):
        for interpreter in interpreter_path_dict:
            setattr(PythonData,
                    f'{interpreter}_data',
                    ProgrammingLanguageData(
                        convert_to_executable_fun=python3_arbitrary_interpreter_convert_to_executable(
                            path_to_interpreter=interpreter_path_dict[interpreter]
                        )
                    ))


python_data = PythonData({'python3': Path('/bin/python3')})

# ============================================ JAVA or SCALA ===========================================================

# TODO
