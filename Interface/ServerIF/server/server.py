import flask
import sys
import markdown


app = flask.Flask(__name__)


@app.route('/')
def init():
    return flask.render_template('root.html')


@app.route('/display_readme')
def display_readme():
    with open('../../../README.md') as readme:
        md = readme.read()
        html = markdown.markdown(md)
    return html


@app.route('/display_problems')
def display_problems():
    return flask.render_template('display_problems.html')


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
