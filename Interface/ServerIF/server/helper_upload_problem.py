import flask
import tempfile
import os
from helper import get_back_to_main_page_html_string
from testing_protocols import TestingProtocol

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

# todo standard short aliases for protocols: to general data json


def upload_inout():
    return assemble_form_enabling_execution_and_conversion_data(
        html_strings=[
            upload_inoutfiles_descr(outfiles_mention_required=True),
            upload_inoutfiles('in'),
            upload_inoutfiles('out')
        ],
        scheme='inout'
    )


def upload_incust():
    return assemble_form_enabling_execution_and_conversion_data(
        html_strings=[
            upload_inoutfiles_descr(outfiles_mention_required=False),
            upload_inoutfiles('in'),
            upload_randin_custchecker_descr('custom checker'),
            upload_randin_custchecker('custom checker'),
        ],
        scheme='incust'
    )


def upload_randcust():
    return assemble_form_enabling_execution_and_conversion_data(
        html_strings=[
            upload_randin_custchecker_descr('custom checker/random input generator'),
            upload_randin_custchecker('custom checker'),
            upload_randin_custchecker('random input generator'),
        ],
        scheme='randcust'
    )


def upload_limited_work_space():
    return assemble_form_enabling_execution_and_conversion_data(
        html_strings=[
            upload_limited_header_footer_description(),
            upload_header_and_footer()
        ],
        scheme='lws'
    )

# ===================================================== UPLOAD =========================================================


def upload_files(semantics, multiple):
    return flask.render_template(
        'upload_problem_templates/form_components/upload/upload_files_button.html',
        semantics=semantics,
        multiple_attr_if_necessary=('multiple' if multiple else '')
    )


def specify_execution_and_conversion_data():
    return flask.render_template(
        'upload_problem_templates/form_components/upload/specify_execution_and_conversion_data.html',
        max_time_limit=20,  # todo export from general data json
        max_memory_limit_megabytes=1000
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


def upload_header_and_footer():
    return upload_files(semantics='head', multiple=False) + upload_files(semantics='foot', multiple=False)

# ================================================== DESCRIPTIONS ======================================================


def upload_inoutfiles_descr(outfiles_mention_required):
    return flask.render_template(
        'upload_problem_templates/form_components/descriptions/upload_inoutfiles_descr.html',
        outfiles_mention_required=outfiles_mention_required
    )


def upload_randin_custchecker_descr(semantics):
    return flask.render_template(
        'upload_problem_templates/form_components/descriptions/upload_randin_custchecker_descr.html',
        semantics=semantics,
        bin_dir_file_count=len(os.listdir('/bin')),
        time_limit=TestingProtocol.HELPER_TIME_LIMIT_SECONDS,
        memory_limit_megabytes=TestingProtocol.HELPER_MEMORY_LIMIT_MEGABYTES
    )


def upload_limited_header_footer_description():
    return flask.render_template(
        'upload_problem_templates/form_components/descriptions/upload_limited_header_footer_description.html'
    )

