import os
import flask
from aux_display_problem import get_path_to_problem_base, get_problem_full_name, get_back_to_main_page_html_string


def display_problem_list():
    problem_ids = sorted(map(int, os.listdir(get_path_to_problem_base())))
    full_names = map(get_problem_full_name, problem_ids)
    problems_info = list(zip(full_names, problem_ids))
    back_link_html_string = get_back_to_main_page_html_string()
    return flask.render_template(
        'display_problem_list.html',
        problems_info=problems_info,
        back_link_html_string=back_link_html_string
    )
