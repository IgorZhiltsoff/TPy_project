from aux import copy_file, create_dir
from random import randint
from problem_data_upload import upload_problem_data


def upload_problem(verbose, path_to_problems_dir):
    # PRE
    problem_id = generate_problem_id()
    path_to_dir = create_problem_dir(problem_id, path_to_problems_dir)

    # INTERACT
    print("You are running a problem upload wizard")
    upload_statement(path_to_dir)

    # HAND OVER CONTROL
    upload_problem_data(verbose, path_to_problems_dir)


def generate_problem_id():
    problem_id = randint(1, 1000)
    if problem_id % 10 == 0:  # multiples of 10 are reserved for preuploaded problems
        problem_id += randint(1, 9)
    return problem_id


def create_problem_dir(problem_id, path_to_problems_dir):
    path_to_dir = f'{path_to_problems_dir}/{problem_id}'
    create_dir(path_to_dir)
    return path_to_dir


def upload_statement(path_to_dir):
    path_to_statement = input("""First, upload a statement. 
Specify a path to .pdf or .txt file (leave blank to skip):""")
    if path_to_statement:
        if path_to_statement.endswith('.pdf'):
            extension = '.pdf'
        elif path_to_statement.endswith('.txt'):
            extension = '.txt'
        else:
            code = input('''Supported extension not detected. Please specify format manually
Type 1 for .txt and 2 for .pdf''')
            extension = ('.pdf' if code == '2' else '.txt')

    copy_file(path_to_statement, f'{path_to_dir}/statement{extension}')

