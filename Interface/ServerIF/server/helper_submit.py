import contextlib
import os
import tempfile
import subprocess
from submission_wizard import label_to_submission_wizard_lang_code
from language_support import LanguageLabel
from helper import pass_input_to_wizard_general


def process_submission(submission_file_storage, problem_id, lang):
    lang_label = eval(lang)
    with tempfile.TemporaryDirectory() as tmp_dir:
        path_to_submission_file = save_submission_file(submission_file_storage, lang_label, tmp_dir)
        with generate_file_to_pass_to_submission_wizard(
                path_to_submission_file=path_to_submission_file,
                problem_id=problem_id,
                lang_label=lang_label) as to_pass:
            return pass_input_to_submission_wizard(to_pass)


def pass_input_to_submission_wizard(to_pass):
    return pass_input_to_wizard_general(
        path_to_wizard='../../CmdLineIF/UploadSubmissionAsStudent/run.sh',
        file_obj_to_pass=to_pass,
        args=['1']
    ).stdout.decode()


@contextlib.contextmanager
def generate_file_to_pass_to_submission_wizard(path_to_submission_file, problem_id, lang_label):
    with tempfile.NamedTemporaryFile('w') as to_pass:
        to_pass.write(f'{problem_id}\n')
        to_pass.write(f'{label_to_submission_wizard_lang_code[lang_label]}\n')
        to_pass.write(f'{path_to_submission_file}\n')
        to_pass.flush()
        to_pass.seek(0)
        yield to_pass


def save_submission_file(submission_file_storage, lang_label, dest_dir):
    path_to_submission_file = os.path.join(dest_dir, generate_submission_name(lang_label))
    submission_file_storage.save(path_to_submission_file)
    return path_to_submission_file


def generate_submission_name(lang_label):
    return f'submission{get_lang_extension(lang_label)}'


def get_lang_extension(lang_label):
    lang_label_to_ext = {
        LanguageLabel.CXX: '.cpp',
        LanguageLabel.CXX11: '.cpp',
        LanguageLabel.CXX14: '.cpp',
        LanguageLabel.CXX17: '.cpp',
        LanguageLabel.CXX20: '.cpp',
        LanguageLabel.PYTHON3: '.py',
        LanguageLabel.HASKELL2010: '.hs',
        LanguageLabel.JAVA: '.java',
        LanguageLabel.SCALA: '.scala'
    }

    return lang_label_to_ext[lang_label]
