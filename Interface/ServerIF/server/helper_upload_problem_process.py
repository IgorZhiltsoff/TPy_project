import tempfile
from helper import pass_input_to_wizard_general

# ===================================================== MASTER =========================================================


def process_problem(form, files):
    with tempfile.TemporaryDirectory() as tmp_dir:
        with tempfile.NamedTemporaryFile('w') as to_pass:
            fill_in_file_to_pass(form, to_pass, files, tmp_dir)
            pass_input_to_problem_upload_wizard(to_pass)


def fill_in_file_to_pass(form, to_pass, files, tmp_dir):
    pass_problem_metadata(form, to_pass, files, tmp_dir)
    define_protocol(form, to_pass)
    pass_execution_and_conversion_data(form, to_pass)
    call_correspondent_passer(form['scheme'], form, to_pass, files, tmp_dir)


def call_correspondent_passer(scheme, form, to_pass, files, tmp_dir):
    # todo export full names from general data (this includes choose_scheme.html)
    return {
        'InputOutput': pass_inout_data,
        'InputCustomChecker': pass_incust_data,
        'RandomInputCustomChecker': pass_randcust_data,
        'LimitedWorkSpace': pass_lws_data
    }[scheme](form, to_pass, files, tmp_dir)


def pass_input_to_problem_upload_wizard(to_pass):
    return pass_input_to_wizard_general(
        path_to_wizard='../../CmdLineIF/UploadProblemAsTeacher/run.sh',
        file_obj_to_pass=to_pass,
        args=[]
    )

# ==================================================== SUBPARTS ========================================================


def pass_problem_metadata(form, to_pass, files, tmp_dir):
    pass


def define_protocol(form, to_pass):
    pass


def pass_execution_and_conversion_data(form, to_pass):
    pass

# ==================================================== SPECIFIC ========================================================


def pass_inout_data(form, to_pass, files, tmp_dir):
    pass


def pass_incust_data(form, to_pass, files, tmp_dir):
    pass


def pass_randcust_data(form, to_pass, files, tmp_dir):
    pass


def pass_lws_data(form, to_pass, files, tmp_dir):
    pass

# ======================================= SUBPARTS FOR SPECIFIC ========================================================


def pass_inoutfiles(form, to_pass, files, tmp_dir, semantics):
    pass


def pass_randgen_custchecker(form, to_pass, files, tmp_dir, semantics):
    pass
