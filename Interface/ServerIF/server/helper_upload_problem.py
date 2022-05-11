import flask
import tempfile
from helper import get_back_to_main_page_html_string

# ===================================================== MASTER =========================================================


def assemble_form_enabling_execution_and_conversion_data(html_strings, scheme):
    return flask.render_template(
        'upload_problem_templates/form_components/form_skeleton.html',
        html_strings=[specify_execution_and_conversion_data()] + html_strings,
        scheme=scheme,
        back_link_html_string=get_back_to_main_page_html_string('I changed my mind!')
    )


def pass_input_to_wizard():
    pass

# ==================================================== SPECIFIC ========================================================


def upload_inout():
    return assemble_form_enabling_execution_and_conversion_data(
        html_strings=[
            upload_inoutfiles_descr(),
            upload_inoutfiles('in'),
            upload_inoutfiles('out')
        ],
        scheme='inout'
    )


def upload_incust():
    pass


def upload_randcust():
    pass


def upload_limited_work_space():
    pass

# ===================================================== UPLOAD =========================================================


def upload_files(semantics, multiple):
    return flask.render_template(
        'upload_problem_templates/form_components/upload/upload_files_button.html',
        semantics=semantics,
        multiple_attr_if_necessary=('multiple' if multiple else '')
    )


def specify_execution_and_conversion_data():
    return flask.render_template(
        'upload_problem_templates/form_components/upload/specify_execution_and_conversion_data.html'
    )


def upload_inoutfiles(semantics):
    return upload_files(
        semantics=semantics,
        multiple=True
    )


def upload_randin_custchecker(semantics):
    return upload_files(
        semantics=semantics,
        multiple=False
    )


def upload_header():
    return upload_files(semantics='head', multiple=False) + upload_files(semantics='foot', multiple=False)

# ================================================== DESCRIPTIONS ======================================================


def upload_inoutfiles_descr():
    pass


def upload_limited_header_footer_description():
    pass


def upload_randin_custchecker_descr():
    pass


for name in ['upload_inoutfiles_descr',
             'upload_limited_header_footer_description',
             'upload_randin_custchecker_descr']:
    exec(
        f'def {name}():'
        f"    return flask.render_template('upload_problem_templates/form_components/descriptions/{name}.html')"
    )
