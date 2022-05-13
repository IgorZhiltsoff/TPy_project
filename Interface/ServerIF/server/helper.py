import flask
import subprocess


def get_back_link_html_string(ref, text):
    return flask.render_template(
        'upper_right_corner_link_template_template.html',
        ref=ref,
        text=text
    )


def get_back_to_main_page_html_string(text):
    return get_back_link_html_string(ref='/', text=text)


def get_back_to_main_page_html_string_standard_text():
    return get_back_to_main_page_html_string(text='Back to main page')


def pass_input_to_wizard_general(path_to_wizard, file_obj_to_pass, args):
    # todo switch to calling "make run"
    file_obj_to_pass.flush()
    file_obj_to_pass.seek(0)
    wizard_invokation = subprocess.run(
        [path_to_wizard, *args],
        stdin=file_obj_to_pass,
        stdout=subprocess.PIPE,
    )
    return wizard_invokation
