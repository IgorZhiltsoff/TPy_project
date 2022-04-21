import os
import tempfile
import subprocess


def process_submission(submission_file_storage, problem_id, lang):
    with tempfile.TemporaryDirectory() as tmp_dir:
        submission_file = save_submission_file(submission_file_storage, lang, tmp_dir)
        with generate_submission_wizard_input(
            path_to_submission_file=submission_file.name,
            problem_id=problem_id,
            lang=lang) as wizard_input:
            pass_input_to_wizard(wizard_input.name)


def pass_input_to_wizard(path_to_wizard_input):
    subprocess.run([''])


def generate_submission_wizard_input(path_to_submission_file, problem_id, lang):
    wizard_input = tempfile.TemporaryFile()
    wizard_input.write(f'{problem_id}\n')
    wizard_input.write(f'{lang}\n')
    wizard_input.write(f'{path_to_submission_file}\n')
    return wizard_input


def save_submission_file(submission_file_storage, lang, dest_dir):
    return submission_file_storage.save(os.path.join(dest_dir, generate_submission_name(lang)))


def generate_submission_name(lang):
    return f'submission{get_lang_extension(lang)}'


def get_lang_extension(lang):
    lang_family_to_ext = {
        "python": '.py',
        "cxx": '.cpp',
        "haskell": '.hs',
        "java": '.java',
        "scala": '.scala'
    }

    lang_family = ''.join(symbol for symbol in lang if not symbol.isdigit())

    return lang_family_to_ext[lang_family]
