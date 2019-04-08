from flask import Flask, jsonify, request, send_from_directory, send_file, g
from http import HTTPStatus
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['DATABASE'] = 'db.sqlite'


@app.route('/dist/<path:path>')
def send_js(path):
    return send_from_directory('dist', path)


@app.route("/")
def home():
    return send_file('html/index.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() == 'lua'


@app.route('/capsule/new', methods=['POST'])
def submit():
    success_count = 0
    for name_field, file in request.files.items():
        print(file)
        if file.filename == '' or not allowed_file(file.filename):
            continue

        filename = secure_filename(file.filename)
        file.save(os.path.join('uploads/', filename))
        success_count += 1

    if success_count > 0:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False}), HTTPStatus.BAD_REQUEST


@app.route('/register', methods=['POST'])
def register():
    success = True
    if success:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False}), HTTPStatus.BAD_REQUEST


if __name__ == "__main__":
    app.run()
