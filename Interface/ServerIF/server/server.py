import sys
import flask
from helper_display_problem import get_back_to_main_page_html_string
from helper_display_problem_info import display_problem_info, md_file_to_html_string
from helper_display_problem_list import display_problem_list
from helper_submit import process_submission
# from helper_upload_problem import


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
    """Responsible for general data input and redirection"""
    if flask.request.form.get('mode') != 'Initiate Problem Upload':
        return flask.render_template(
            'upload_problem_templates/upload_problem_metadata.html',
            back_link_html_string=get_back_to_main_page_html_string()
        )
    else:
        protocols_cnt = int(flask.request.form.get('protocols_cnt'))
        for protocol_idx in range(protocols_cnt):
            flask.redirect('/upload_protocol_master')


@app.route('/upload_protocol_master', methods=['GET', 'POST'])
def upload_protocol_master():
    if flask.request.form.get('mode') != 'Specify Protocol Metadata':
        return flask.render_template('upload_problem_templates/upload_protocol_metadata.html')
    else:
        scheme = flask.request.form.get('scheme')
        test_cnt = int(flask.request.form.get('test_cnt'))
        supported_langs_cnt = int(flask.request.form.get('supported_langs_cnt'))
        for supported_lang_idx in range(supported_langs_cnt):
            upload_execution_and_conversion_data()


@app.route('/upload_execution_and_conversion_data', methods=['GET', 'POST'])
def upload_execution_and_conversion_data():
    if flask.request.form.get('mode') != 'Upload Execution and Conversion Data':
        return flask.render_template('upload_problem_templates/upload_execution_and_conversion_data.html')
    else:
        return 'haha'


@app.route('/upload_inout', methods=['GET', 'POST'])
def upload_inout():
    pass


@app.route('/upload_incustom', methods=['GET', 'POST'])
def upload_incustom():
    pass


@app.route('/upload_randcustom', methods=['GET', 'POST'])
def upload_randcustom():
    pass


@app.route('/upload_limited_work_space', methods=['GET', 'POST'])
def upload_limited_work_space():
    pass


if __name__ == '__main__':
    # address = sys.argv[1]
    # port = int(sys.argv[2])
    # app.run(address, port, debug=True)
    address = 'localhost'
    port = 5000
    app.run(address, port, debug=True)
