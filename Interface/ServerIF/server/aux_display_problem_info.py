import os.path
import fitz
import markdown
from lxml import etree
from aux_display_problem \
    import get_problem_data_dict, get_path_to_problem_dir, get_problem_full_name, generate_html_tag, \
    get_html_tree, append_child_to_body, prepend_child_to_body


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


def pdf_file_to_html_string(path_to_statement):
    html = ''
    with fitz.open(path_to_statement) as doc:
        for num, page in enumerate(doc):
            html += page.getText("html")
    return html


def md_file_to_html_string(path_to_statement):
    with open(path_to_statement) as doc:
        md = doc.read()
        html = markdown.markdown(md)
    return html


def txt_file_to_html_string(path_to_statement):
    with open(path_to_statement) as doc:
        return f'<html><body><p>{doc.read()}</p></body></html>'


def generate_heading_html_tag(problem_id):
    return generate_html_tag(
        descriptor='h1',
        text=get_problem_full_name(problem_id)
    )


def prepend_heading_html_tag(heading_html_tag, tree):
    prepend_child_to_body(
        new=heading_html_tag,
        tree=tree
    )


def generate_return_link_html_tag():
    return generate_html_tag(
        descriptor='a',
        text='Return to problems list',
        href="display_problems"
    )


def append_return_link_html_tag(return_link_html_tag, tree):
    append_child_to_body(
        new=return_link_html_tag,
        tree=tree
    )


def display_problem_info(problem_id):
    tree = get_html_tree(get_problem_statement_html_string(problem_id))
    heading_html_tag = generate_heading_html_tag(problem_id)
    return_link_html_tag = generate_return_link_html_tag()

    prepend_heading_html_tag(
        heading_html_tag=heading_html_tag,
        tree=tree
    )

    append_return_link_html_tag(
        return_link_html_tag=return_link_html_tag,
        tree=tree
    )

    return etree.tostring(tree).decode('utf-8')
