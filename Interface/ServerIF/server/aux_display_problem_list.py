import os
from lxml import etree
from aux_display_problem import \
    get_path_to_problem_base, get_problem_full_name, get_html_tree, \
    append_child_to_body, prepend_child_to_body, generate_html_tag


def display_problem_list():
    problem_ids = sorted(map(int, os.listdir(get_path_to_problem_base())))
    tree = generate_list_skeleton_tree()
    for problem_id in problem_ids:
        paragraph = generate_problem_paragraph_link_tag(problem_id)
        append_child_to_body(
            new=paragraph,
            tree=tree
        )

    append_child_to_body(
        new=generate_back_to_main_page_link_tag(),
        tree=tree
    )

    return etree.tostring(tree).decode('utf-8')


def generate_list_skeleton_tree():
    html = '<html><body><h1>List of uploaded problems:</h1></body></html>'
    return get_html_tree(html)


def generate_problem_paragraph_link_tag(problem_id):
    paragraph = etree.Element('p')
    etree.SubElement(
        _parent=paragraph,
        _tag='a',
        href=f"display_problems?problem_id={problem_id}"
    ).text = get_problem_full_name(problem_id)
    return paragraph


def generate_back_to_main_page_link_tag():
    return generate_html_tag(
        descriptor='a',
        text='Back to main page',
        href="/"
    )
