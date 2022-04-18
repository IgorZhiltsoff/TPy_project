import os
from aux_display_problem import get_path_to_problem_base


def display_problem_list():
    problem_ids = os.listdir(get_path_to_problem_base())


def generate_problem_link(problem_id):
    pass
