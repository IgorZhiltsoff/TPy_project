import sys
import os
import flask
from helper_display_problem import get_back_to_main_page_html_string
from helper_display_problem_info import display_problem_info, md_file_to_html_string
from helper_display_problem_list import display_problem_list
from helper_submit import process_submission


app = flask.Flask(__name__)


@app.route('/')
def init():
    return flask.render_template('root.html')


@app.route('/display_readme')
def display_readme():
    return flask.render_template(
        'display_readme.html',
        readme_html_string=md_file_to_html_string('../../../README.md'),
        back_link_html_string=get_back_to_main_page_html_string()
    )


@app.route('/display_problems')
def display_problems():
    problem_id = flask.request.args.get('problem_id')
    if not problem_id:
        return display_problem_list()
    else:
        problem_id = int(problem_id)
        return display_problem_info(problem_id)


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if flask.request.form.get('mode') != 'Submit':
        return flask.render_template(
            'submit.html',
            back_link_html_string=get_back_to_main_page_html_string()
        )
    else:
        return process_submission(
            submission_file_storage=flask.request.files['submission'],
            problem_id=flask.request.form['problem_id'],
            lang=flask.request.form['lang']
        )


@app.route('/upload_problem', methods=['GET', 'POST'])
def upload_problem():
    return flask.render_template(
        'upload_problem_templates/choose_protocol_scheme.html',
        semantics='header',
        time_limit=10,
        memory_limit_megabytes=1536
        #'upload_problem_templates/upload_specific_protocol_templates/upload_randin_custchecker_template.html',
        #semantics='custom checker',
        #bin_dir_file_count=len(os.listdir('/bin')),
        #time_limit=10,
        #memory_limit_megabytes=1536
    )
    #if not flask.request.form.get('mode'):
    #    return flask.render_template(
    #        'upload_problem_templates/upload_problem_metadata.html',
    #        back_link_html_string=get_back_to_main_page_html_string()
    #    )
    #elif flask.request.form.get('mode') == 'Upload Metadata':
    #    return flask.render_template('upload_problem_templates/choose_protocol_scheme.html')
    #elif flask.request.form.get('mode') == 'Choose Protocol Scheme':
    #    return ''


if __name__ == '__main__':
    address = sys.argv[1]
    port = int(sys.argv[2])
    app.run(address, port, debug=True)
