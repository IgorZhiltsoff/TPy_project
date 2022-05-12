import tempfile

# ===================================================== MASTER =========================================================


def pass_input_to_wizard(form, files):
    with tempfile.TemporaryDirectory() as tmp_dir:
        with tempfile.NamedTemporaryFile('w') as wizard_input:
            pass


# ==================================================== SUBPARTS ========================================================


def pass_problem_metadata(form, files):
    pass


def define_protocol(form):
    pass


def pass_execution_and_conversion_data(form):
    pass

# ==================================================== SPECIFIC ========================================================

def pass_inout_data(files):
    pass


def pass_incust_data(files):
    pass


def pass_randcust_data(files):
    pass


def pass_lws_data(files):
    pass

# ======================================= SUBPARTS FOR SPECIFIC ========================================================


def pass_inoutfiles(files, semantics):
    pass


def pass_randgen_custchecker(files, semantics):
    pass
