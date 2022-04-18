import flask
import sys
import markdown
from aux import display_problem_list, display_problem_info, md_file_to_html_string


app = flask.Flask(__name__)


@app.route('/')
def init():
    return flask.render_template('root.html')


@app.route('/display_readme')
def display_readme():
    return md_file_to_html_string('../../../README.md')


@app.route('/display_problems')
def display_problems():
    problem_id = flask.request.args.get('problem_id')
    if not problem_id:
        return display_problem_list()
    else:
        problem_id = int(problem_id)
        return display_problem_info(problem_id)


@app.route('/submit')
def submit():
    pass


@app.route('/upload_problem')
def upload_problem():
    pass


if __name__ == '__main__':
    address = sys.argv[1]
    port = int(sys.argv[2])
    app.run(address, port, debug=True)
