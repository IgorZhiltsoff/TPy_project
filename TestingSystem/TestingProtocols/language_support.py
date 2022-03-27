# this module defines language support objects

from testing_protocols import ProgrammingLanguageData
import subprocess

# ================================================= CXX ================================================================


def cxx_arbitrary_std_convert_to_executable(cxx_standard):
    def cxx_fixed_std_convert_to_executable(path_to_src, suggested_exec_name, conversion_opts=None):
        conversion_opts = conversion_opts if conversion_opts else []

        subprocess.run(['g++', '-o', suggested_exec_name, f'-std=c++{cxx_standard}'] + conversion_opts + [path_to_src])
        return suggested_exec_name
    return cxx_fixed_std_convert_to_executable


cxx11_data = ProgrammingLanguageData(convert_to_executable_fun=cxx_arbitrary_std_convert_to_executable(11))
cxx14_data = ProgrammingLanguageData(convert_to_executable_fun=cxx_arbitrary_std_convert_to_executable(14))
cxx17_data = ProgrammingLanguageData(convert_to_executable_fun=cxx_arbitrary_std_convert_to_executable(17))
cxx20_data = ProgrammingLanguageData(convert_to_executable_fun=cxx_arbitrary_std_convert_to_executable(20))

# =============================================== HASKELL ==============================================================


def haskell_convert_to_executable(path_to_src, suggested_exec_name, conversion_opts=None):
    pass


haskell_data = ProgrammingLanguageData(convert_to_executable_fun=haskell_convert_to_executable)

# =============================================== PYTHON3 ==============================================================


def python3_arbitrary_interpreter_convert_to_executable(interpreter):
    def python3_fixed_interpreter_convert_to_executable(path_to_src, suggested_exec_name, conversion_opts=None):
        pass
    return python3_fixed_interpreter_convert_to_executable


...

# ============================================ JAVA or SCALA ===========================================================
