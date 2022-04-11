from problem_data_retriever import retrieve_problem_data
from testing_protocols import UserSubmittedData
from random import randint


def submission_wizard(path_to_problems_dir):
    problem_id = input('Choose problem to solve (specify problem id): ')
    problem_data = retrieve_problem_data(problem_id, path_to_problems_dir)

    path_to_src = input('Submit path to solution: ')
    user_submitted_data = UserSubmittedData(path_to_src=path_to_src, submission_id=randint(1, 1000))

    print(problem_data.check(user_submitted_data))
