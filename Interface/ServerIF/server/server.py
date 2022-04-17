import flask
import sys

address = sys.argv[0]
port = sys.argv[1]

app = flask.Flask(__name__)


@app.route('/')
def init():
    return flask.render_template('root.html')


@app.route('/display_readme')
def display_readme():
    return flask.render_template('display_readme.html')


@app.route('/display_problems')
def display_problems():
    return flask.render_template('display_problems.html')


@app.route('/submit')
def submit():
    pass


@app.route('/upload_problem')
def upload_problem():
    pass
