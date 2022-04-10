import UploadProblemAsTeacher.upload_wizard.problem_data_upload.protocol_upload_wizard.inout
import UploadProblemAsTeacher.upload_wizard.problem_data_upload.protocol_upload_wizard.in_custom
import UploadProblemAsTeacher.upload_wizard.problem_data_upload.protocol_upload_wizard.rand_custom
import UploadProblemAsTeacher.upload_wizard.problem_data_upload.protocol_upload_wizard.limited_work_space
from UploadProblemAsTeacher.upload_wizard.aux import create_dir


def upload_protocol(path_to_dir, protocol_number, custodian, verbose):
    # PRE
    key_seq_to_current_dict = ('protocols', str(protocol_number))
    path_to_protocol_dir = create_dir(f'{path_to_dir}/prot{protocol_number}')

    # INTERACT
    upload_programming_language_data(key_seq_to_current_dict, custodian)
    scheme = choose_protocol_scheme(key_seq_to_current_dict, custodian, verbose)
    for opts_type in ['conversion options', 'command_line options']:
        upload_opts(opts_type, key_seq_to_current_dict, custodian)

    # HAND OVER CONTROL
    eval(f'{scheme}.upload_specific_protocol')(path_to_protocol_dir, key_seq_to_current_dict, custodian, verbose)


def upload_programming_language_data(key_seq_to_current_dict, custodian):
    language_code = input("""Choose one of 2 supported languages:
    Type 1 for C++
    Type 2 for Python3
    """)

    if language_code == '1':
        std = input("Specify C++ standard (available: 11, 14, 17, 20): ")
        programming_language_data = f'cxx_data.cxx{std}_data'
    else:
        programming_language_data = 'python_data.python3_data'

    custodian.nested_fill_in(key_seq_to_current_dict + ('programming_language_data', ), programming_language_data)


def choose_protocol_scheme(key_seq_to_current_dict, custodian, verbose):
    test_count = int(input("Input test count: N="))
    custodian.nested_fill_in(key_seq_to_current_dict + ('test_count', ), test_count)
    if verbose:
        prompt = """
Input protocol scheme, choosing one of 4 options:
    1. InputOutput: requires N input files and N files with correct outputs. 
        The system will run submission on each input and check whether it's equal to corresponding correct output
        
    2. InputCustomChecker: requires N input files and 1 custom checker executable
         The system will run submission on each input and check output with custom checker
         
    3. RandomInputCustomChecker: requires 1 random input generator, 1 custom checker executable and 1
        The system will generate N random inputs, run submission on all of them and check output with custom checker
    
    4. LimitedWorkSpace: requires 1 "header", 1 "footer" and 1 string denoting file extension (see below)
        The system will take submission source and merge it with header and footer into a compound file:
            <header>
            <submission src>
            <footer>
        Thus, to save this file, we need to know the correct extension for it
        Upon execution, the compound file should print 1 if the submission has passed and 0 otherwise

Input the number of desired protocol: """
    else:
        prompt = """
Input 1 for InputOutput, 
      2 for InputCustomChecker,
      3 for RandomInputCustomChecker,
      4 for LimitedWorkSpace:
"""

    scheme = {'1': 'inout', '2': 'in_custom', '3': 'rand_custom', '4': 'limited_work_space'}[input(prompt)]
    custodian.nested_fill_in(key_seq_to_current_dict + ('scheme', ), scheme)
    return scheme


def upload_opts(opts_type, key_seq_to_current_dict, custodian):
    opts = input(f"Input {opts_type} options (leave blank to skip): ").split()
    custodian.nested_fill_in(key_seq_to_current_dict + (opts_type, ), opts)
