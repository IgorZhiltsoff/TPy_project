from UploadProblemAsTeacher.upload_wizard.helper import copy_file, create_dir, get_path_suffix
from random import randint
from UploadProblemAsTeacher.upload_wizard.problem_data_upload import upload_problem_data
from data_custodian import JsonDataCustodian
import os.path


def upload_problem(path_to_problems_dir, verbose, wizard_version_running):
    # PRE
    print(f"You are running a problem upload wizard v{wizard_version_running}")
    custodian.fill_in("uploaded_by_wizard_version", wizard_version_running)

    problem_id = generate_problem_id()
    print(f"\033[92mProblem received id: {problem_id}\033[0m")
    path_to_dir = create_problem_dir(problem_id, path_to_problems_dir)
    custodian = JsonDataCustodian(path_to_dir, 'problem_data')

    # INTERACT
    upload_statement_and_name(custodian, path_to_dir)

    # HAND OVER CONTROL
    upload_problem_data(custodian, path_to_dir, verbose)


def generate_problem_id():
    problem_id = randint(1, 1000)
    if problem_id % 10 == 0:  # multiples of 10 are reserved
        problem_id += randint(1, 9)
    return problem_id


def create_problem_dir(problem_id, path_to_problems_dir):
    path_to_dir = f'{path_to_problems_dir}/{problem_id}'
    create_dir(path_to_dir)
    return path_to_dir


def upload_statement_and_name(custodian, path_to_dir):
    supported_extensions = {'.md', '.pdf', '.txt'}
    name = input("Give your problem a concise and clear name: ")
    path_to_statement = input("""Upload a statement. 
Specify a path to .md, .pdf or .txt file (leave blank to skip): """)
    filename, extension = os.path.splitext(path_to_statement)
    if extension not in supported_extensions:
        code = input('''Supported extension not detected. Please specify format manually
Type 1 for .txt, 2 for .pdf and 3 for .md''')
        extension = {1: '.txt', 2: '.pdf', 3: '.md'}[int(code)]

    path_to_statement_copy = f'{path_to_dir}/statement{extension}'
    copy_file(path_to_statement, path_to_statement_copy)

    custodian.fill_in('name', name)
    custodian.fill_in('statement file extension', extension)
    custodian.fill_in('path to statement', get_path_suffix(path_to_statement_copy))
