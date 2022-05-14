import os.path
import tempfile
import werkzeug.datastructures
import contextlib
import re
from helper import pass_input_to_wizard_general

# ===================================================== MASTER =========================================================


def process_problem(form: werkzeug.datastructures.MultiDict,
                    files: werkzeug.datastructures.MultiDict):
    with tempfile.TemporaryDirectory() as tmp_dir:
        with file_to_pass(form, files, tmp_dir) as to_pass:
            return pass_input_to_problem_upload_wizard(to_pass)


@contextlib.contextmanager
def file_to_pass(form, files, tmp_dir):
    with tempfile.NamedTemporaryFile('w') as to_pass:
        to_pass.writeln = lambda data: to_pass.write(data + '\n')
        fill_in_file_to_pass(form, to_pass, files, tmp_dir)
        yield to_pass


def fill_in_file_to_pass(form, to_pass, files, tmp_dir):
    pass_problem_metadata(form, to_pass, files, tmp_dir)
    specify_general_protocol_data(form, to_pass)
    call_correspondent_passer(form['scheme'], to_pass, files, tmp_dir)
    to_pass.write('n')  # indicator that it was the last protocol to be uploaded


def call_correspondent_passer(scheme, to_pass, files, tmp_dir):
    # todo export full names from general data (this includes choose_scheme.html)
    return {
        'inout': pass_inout_data,
        'incust': pass_incust_data,
        'randcust': pass_randcust_data,
        'lws': pass_lws_data
    }[scheme](to_pass, files, tmp_dir)


def pass_input_to_problem_upload_wizard(to_pass):
    out = pass_input_to_wizard_general(
        path_to_wizard='../../CmdLineIF/UploadProblemAsTeacher/run.sh',
        file_obj_to_pass=to_pass,
        args=[]
    ).stdout.decode().split('\n')
    wizard_version = out[0]
    problem_id = out[1][5:-3]  # todo smarter trimming
    return f'<html><p>{wizard_version}</p><p>Problem received id: {problem_id}</p></html>'

# ==================================================== SUBPARTS ========================================================


def pass_problem_metadata(form, to_pass, files, tmp_dir):
    to_pass.writeln(form['name'])
    stored_statement = werkzeug.datastructures.FileStorage(files['statement'])
    extension = form['ext']
    path_to_statement = os.path.join(tmp_dir, f"statement{extension}")
    stored_statement.save(path_to_statement)
    to_pass.writeln(path_to_statement)


def specify_general_protocol_data(form, to_pass):
    test_cnt = form['test_cnt']
    scheme = {'inout': '1', 'incust': '2', 'randcust': '3', 'lws': '4'}[form['scheme']]  # todo scheme codes from general data
    supported_languages_cnt = form['supported_languages_cnt']
    to_pass.writeln(test_cnt)
    to_pass.writeln(scheme)
    to_pass.writeln(supported_languages_cnt)
    pass_execution_and_conversion_data(form, to_pass)


def pass_execution_and_conversion_data(form, to_pass):
    to_pass.writeln(form['lang_repr'])
    to_pass.writeln(form['conversion_opts'])
    to_pass.writeln(form['command_line_opts'])
    to_pass.writeln(form['time_limit'])
    to_pass.writeln(form['memory_limit_megabytes'])

# ==================================================== SPECIFIC ========================================================


def pass_inout_data(to_pass: tempfile.NamedTemporaryFile,
                    files: werkzeug.datastructures.MultiDict,
                    tmp_dir: str):
    pass_multiple_files(to_pass, files, tmp_dir, 'in')
    pass_multiple_files(to_pass, files, tmp_dir, 'out')


def pass_incust_data(to_pass, files, tmp_dir):
    pass_multiple_files(to_pass, files, tmp_dir, 'in')
    pass_single_file(to_pass, files, tmp_dir, 'custom checker')


def pass_randcust_data(to_pass, files, tmp_dir):
    pass_single_file(to_pass, files, tmp_dir, 'random input generator')
    pass_single_file(to_pass, files, tmp_dir, 'custom checker')


def pass_lws_data(to_pass, files, tmp_dir):
    pass_single_file(to_pass, files, tmp_dir, 'head')
    pass_single_file(to_pass, files, tmp_dir, 'foot')

# ======================================= SUBPARTS FOR SPECIFIC ========================================================


def pass_multiple_files(to_pass: tempfile.NamedTemporaryFile,
                        files: werkzeug.datastructures.MultiDict,
                        tmp_dir: str,
                        semantics: str):
    storages = files.getlist(semantics)
    storages.sort(key=lambda storage: storage.filename)  # to be able to write paths to to_pass as we save files
    for storage in storages:
        path_to_file = os.path.join(tmp_dir, storage.filename)
        storage.save(path_to_file)
        to_pass.writeln(path_to_file)


def pass_single_file(to_pass: tempfile.NamedTemporaryFile,
                     files: werkzeug.datastructures.MultiDict,
                     tmp_dir: str,
                     semantics: str):
    storage = files[semantics]
    path_to_file = os.path.join(tmp_dir, storage.filename)
    storage.save(path_to_file)
    to_pass.writeln(path_to_file)
