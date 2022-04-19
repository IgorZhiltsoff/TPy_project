import json
import os.path
from lxml import etree
from io import StringIO


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


def generate_html_tag(descriptor, text, attribute=None, **kwargs):
    tag = etree.Element(descriptor, attribute, **kwargs)
    tag.text = text
    return tag


def get_html_tree(html):
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html), parser)
    return tree


def get_tree_body(tree):
    return tree.find('body')


def append_sibling(new, sibling):  # todo unify
    return sibling.addnext(new)