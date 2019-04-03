from flask import Flask, request, send_from_directory, send_file
from http import HTTPStatus
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)


@app.route('/dist/<path:path>')
def send_js(path):
    return send_from_directory('dist', path)


@app.route("/")
def home():
    return send_file('html/index.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() == 'lua'


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part', HTTPStatus.BAD_REQUEST
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return 'No selected file', HTTPStatus.BAD_REQUEST
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'success', 200


if __name__ == "__main__":
    app.run()
