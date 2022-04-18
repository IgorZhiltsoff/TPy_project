import fitz
import markdown
from lxml import etree
from io import StringIO, BytesIO


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


def md_file_to_html_string(filepath):
    with open(filepath) as doc:
        md = doc.read()
        html = markdown.markdown(md)
    return html


def txt_file_to_html_string(filepath):
    with open(filepath) as doc:
        return doc.read()


def append_heading_html_tag(heading, html):
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html), parser)
    body = tree.find('body')
    first_paragraph = body.getchildren()[0]
    first_paragraph.addprevious(heading)


def generate_heading_html_tag(proper_name, problem_id):
    heading = etree.Element('h1')
    heading.text = f'Problem #{problem_id}: {proper_name}'
    return heading
