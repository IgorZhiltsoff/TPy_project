import json
import os.path
import fitz
import markdown
from lxml import etree
from io import StringIO, BytesIO


def get_path_to_problem_dir(problem_id):
    return f'../../../problems_base/{problem_id}'


def get_problem_data_dict(problem_id):
    problem_dir = get_path_to_problem_dir(problem_id)
    with open(os.path.join(problem_dir, 'problem_data.json')) as data:
        problem_data_dict = json.load(data)
    return problem_data_dict


def get_problem_name(problem_id):
    problem_data_dict = get_problem_data_dict(problem_id)
    return problem_data_dict['name']


def get_statement_extension(problem_id):
    problem_data_dict = get_problem_data_dict(problem_id)
    return problem_data_dict['statement file extension']


def get_statement_filename(problem_id):
    return f'statement{get_statement_extension(problem_id)}'


def get_problem_statement_html_string(problem_id):
    ext_to_file_parser = {'.md': md_file_to_html_string,
                          '.pdf': pdf_file_to_html_string,
                          '.txt': txt_file_to_html_string}

    ext = get_statement_extension(problem_id)
    path_to_statement = os.path.join(get_path_to_problem_dir(problem_id), get_statement_filename(problem_id))
    file_to_html_string = ext_to_file_parser[ext]

    return file_to_html_string(path_to_statement)


def pdf_file_to_html_string(filepath):
    html = ''
    with fitz.open(filepath) as doc:
        for num, page in enumerate(doc):
            html += page.getText("html")
    return html


def md_file_to_html_string(filepath):
    with open(filepath) as doc:
        md = doc.read()
        html = markdown.markdown(md)
    return html


def txt_file_to_html_string(filepath):
    with open(filepath) as doc:
        return f'<html><body><p>{doc.read()}</p></body></html>'


def generate_heading_html_tag(name, problem_id):
    heading = etree.Element('h1')
    heading.text = f'Problem #{problem_id}: {name}'
    return heading


def get_html_tree(html):
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html), parser)
    return tree


def get_tree_body(tree):
    return tree.find('body')


def prepend_heading_html_tag(heading_html_tag, html):
    tree = get_html_tree(html)
    body = get_tree_body(tree)
    first_item = body.getchildren()[0]
    first_item.addprevious(heading_html_tag)
    return etree.tostring(tree).decode('utf-8')


def generate_return_link_html_tag():
    return_link = etree.Element('a', href="display_problems")
    return_link.text = 'Return to problems list'
    return return_link


def append_return_link_html_tag(return_link_html_tag, html):
    tree = get_html_tree(html)
    body = get_tree_body(tree)
    last_item = body.getchildren()[-1]
    last_item.addnext(return_link_html_tag)
    return etree.tostring(tree).decode('utf-8')


def display_problem_list():
    pass


def display_problem_info(problem_id):
    name = get_problem_name(problem_id)
    heading_html_tag = generate_heading_html_tag(name, problem_id)
    return_link_html_tag = generate_return_link_html_tag()
    html_with_heading = prepend_heading_html_tag(
        heading_html_tag=heading_html_tag,
        html=get_problem_statement_html_string(problem_id)
    )
    full_html = append_return_link_html_tag(
        return_link_html_tag=return_link_html_tag,
        html=html_with_heading
    )
    return full_html
