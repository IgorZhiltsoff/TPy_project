import os
from problem_data_retriever import retrieve_problem_data
from testing_protocols import UserSubmittedData
from language_support import LanguageLabel
from random import randint


def submission_wizard(path_to_problems_dir, mount_point):
    problem_id = input('Choose problem to solve (specify problem id): ')
    problem_data = retrieve_problem_data(problem_id, path_to_problems_dir, mount_point)

    label_code = input("Choose programming language from list:"
                       "1. Python3.10"
                       "2. C++11"
                       "3. C++14"
                       "4. C++17"
                       "5. C++20")
    code_to_label = {
        "1": LanguageLabel.PYTHON3,
        "2": LanguageLabel.CXX11,
        "3": LanguageLabel.CXX14,
        "4": LanguageLabel.CXX17,
        "5": LanguageLabel.CXX20,
    }
    label = code_to_label[label_code]

    path_to_src = os.path.expanduser(input('Submit path to solution: '))
    user_submitted_data = UserSubmittedData(path_to_src=path_to_src, submission_id=randint(1, 1000), label=label)

    print(problem_data.check(user_submitted_data))
