import flask
import tempfile

# ==================================================== PROCESSOR =======================================================


def pass_input_to_wizard():
    pass

# ==================================================== SPECIFIC ========================================================


def upload_inout():
    return upload_inoutfiles_template('in') + upload_inoutfiles_template('out')


def upload_incust():
    pass


def upload_randcust():
    pass


def upload_limited_work_space():
    pass

# ==================================================== SUBPARTS ========================================================


def upload_inoutfiles_template(semantics):
    return flask.render_template(
        'upload_problem_templates/upload_specific_protocol_templates/upload_inoutfiles_template.html',
        semantics=semantics
    )


def upload_randin_custchecker_template(semantics):
    pass


def upload_header_footer_template(semantics):
    pass
