import fitz


def get_problem_name():
    pass


def display_problem_list():
    pass


def display_problem_info(problem_id):
    pass

def pdf_file_to_html_string(filepath):
    html = ''
    with fitz.open(filepath) as doc:
        for num, page in enumerate(doc):
            html += page.getText("html")
    return html
