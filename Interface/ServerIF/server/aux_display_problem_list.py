import os
from lxml import etree
from aux_display_problem import \
    get_path_to_problem_base, get_problem_full_name, generate_html_tag, get_html_tree, get_tree_body


def display_problem_list():
    problem_ids = os.listdir(get_path_to_problem_base())
    tree = generate_list_skeleton_tree()
    body = get_tree_body(tree)
    for problem_id in problem_ids:
        paragraph = etree.SubElement(body, 'p')
        etree.SubElement(
            _parent=paragraph,
            _tag='a',
            href=f"display_problems?problem_id={problem_id}"
        ).text = get_problem_full_name(problem_id)

    return etree.tostring(tree).decode('utf-8')


def generate_list_skeleton_tree():
    html = '<html><body><h1>List of uploaded problems:</h1></body></html>'
    return get_html_tree(html)
