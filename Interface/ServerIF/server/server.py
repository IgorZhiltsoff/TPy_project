import sys
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
    return 'Not working'


if __name__ == '__main__':
    # address = sys.argv[1]
    # port = int(sys.argv[2])
    # app.run(address, port, debug=True)
    address = 'localhost'
    port = 5000
    app.run(address, port, debug=True)
