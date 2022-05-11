import flask


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
