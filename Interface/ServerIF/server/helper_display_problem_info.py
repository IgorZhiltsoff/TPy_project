import os.path
import fitz
import flask
import markdown
from helper_display_problem import \
    get_problem_data_dict, get_path_to_problem_dir, get_problem_full_name
from helper import get_back_link_html_string


def display_problem_info(problem_id):
    full_name = get_problem_full_name(problem_id)
    statement_html_string = get_problem_statement_html_string(problem_id)
    back_link_html_string = get_back_link_html_string(ref='display_problems', text='Back to problems list')
    return flask.render_template(
        'display_problems_templates/display_problem_info.html',
        problem_id=problem_id,
        full_name=full_name,
        statement_html_string=statement_html_string,
        back_link_html_string=back_link_html_string
    )


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
        return doc.read()
