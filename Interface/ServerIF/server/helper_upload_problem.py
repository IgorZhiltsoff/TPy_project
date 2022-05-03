import tempfile

# ==================================================== PROCESSOR =======================================================
import flask


def pass_input_to_wizard():
    pass


def protocol_metadata_upload_html_list_generator(protocols_cnt):
    return [flask.render_template(
        'upload_problem_templates/upload_protocol_metadata.html',
        idx=idx
    ) for idx in range(protocols_cnt)]


def html_list_generator():
    return [(flask.render_template(

    )]

def scheme_to_template(scheme):
    return {
        'InputOutput': 'forms/upload_specific_protocols_templates',
        'InputCustomChecker': ,
        'RandomInputCustomChecker': ,
        'LimitedWorkSpace': ,
    }

# ==================================================== GENERAL =========================================================


def upload_execution_and_conversion_data():
    pass


def upload_problem_metadata():
    pass


def choose_protocol_scheme():
    pass

# ==================================================== SPECIFIC ========================================================


def upload_inout():
    pass


def upload_incust():
    pass


def upload_randcust():
    pass


def upload_limited_work_space():
    pass

# ==================================================== SUBPARTS ========================================================


def upload_inoutfiles_template(semantics):
    pass


def upload_randin_custchecker_template(semantics):
    pass


def upload_header_footer_template(semantics):
    pass

