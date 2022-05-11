import os
from problem_data_retriever import retrieve_problem_data
from testing_protocols import UserSubmittedData
from language_support import LanguageLabel
from random import randint


submission_wizard_lang_code_to_label = {  # todo export from general data json
    "1.1": LanguageLabel.CXX11,
    "1.2": LanguageLabel.CXX14,
    "1.3": LanguageLabel.CXX17,
    "1.4": LanguageLabel.CXX20,
    "2": LanguageLabel.PYTHON3,
}

label_to_submission_wizard_lang_code = {label: code for code, label in submission_wizard_lang_code_to_label.items()}


def submission_wizard(path_to_problems_dir, silent, mount_point):
    problem_id = input('Choose problem to solve (specify problem id): ' if not silent else '')
    problem_data = retrieve_problem_data(problem_id, path_to_problems_dir, mount_point)

    label_code = input("Choose programming language from list:"
                       "1.1. C++11"
                       "1.2. C++14"
                       "1.3. C++17"
                       "1.4. C++20"
                       "2. Python3.10" if not silent else '')
    label = submission_wizard_lang_code_to_label[label_code]

    path_to_src = os.path.expanduser(input('Submit path to solution: ' if not silent else ''))
    user_submitted_data = UserSubmittedData(path_to_src=path_to_src, submission_id=randint(1, 1000), label=label)

    print(problem_data.check(user_submitted_data))
