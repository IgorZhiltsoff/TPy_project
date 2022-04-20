import json
import os.path
import flask


def get_path_to_problem_base():
    return f'../../../problems_base'


def get_path_to_problem_dir(problem_id):
    return os.path.join(get_path_to_problem_base(), str(problem_id))


def get_problem_data_dict(problem_id):
    path_to_problem_dir = get_path_to_problem_dir(problem_id)
    with open(os.path.join(path_to_problem_dir, 'problem_data.json')) as data:
        problem_data_dict = json.load(data)
    return problem_data_dict


def get_problem_name(problem_id):
    problem_data_dict = get_problem_data_dict(problem_id)
    return problem_data_dict['name']


def get_problem_full_name(problem_id):
    return f'Problem #{problem_id}: {get_problem_name(problem_id)}'


def get_back_link_html_string(ref, text):
    return flask.render_template(
        'upper_right_corner_link_template_template.html',
        ref=ref,
        text=text
    )


def get_back_to_main_page_html_string():
    return get_back_link_html_string(ref='/', text='Back to main page')
