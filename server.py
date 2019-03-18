from flask import Flask, send_from_directory, send_file
from http import HTTPStatus

app = Flask(__name__)


@app.route('/dist/<path:path>')
def send_js(path):
    return send_from_directory('dist', path)


@app.route("/")
def home():
    return send_file('html/index.html')


@app.route('/submit', methods=['POST'])
def submit():
    return 'gj mate'


if __name__ == "__main__":
    app.run()
