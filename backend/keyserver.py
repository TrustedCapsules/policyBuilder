from flask import Flask, jsonify, request, send_from_directory, send_file, g
from http import HTTPStatus
from werkzeug.utils import secure_filename
import os
from backend.req_parser import *
from backend import db

app = Flask(__name__)
app.config['DATABASE'] = 'db.sqlite'
app.config['TESTING'] = True


@app.route('/dist/<path:path>')
def send_js(path):
    return send_from_directory('dist', path)


@app.route("/")
def home():
    return send_file('html/index.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() == 'lua'


@app.route('/capsule', methods=['POST'])
def capsule():
    is_lua_uploaded = False
    filename = None
    for name_field, file in request.files.items():
        if file.filename == '' or not allowed_file(file.filename):
            continue

        filename = secure_filename(file.filename)
        file.save(os.path.join('uploads/', filename))
        is_lua_uploaded = True
        break

    if not is_lua_uploaded:
        return jsonify({"success": False, "msg": "No lua file"}), HTTPStatus.BAD_REQUEST

    data = request.form.to_dict()
    if not CapsuleRequest.is_valid(data):
        return jsonify({"success": False, "msg": "Invalid form data"}), HTTPStatus.BAD_REQUEST

    print('filename is:', filename)
    cap_req = CapsuleRequest(request.form, filename)
    print('capreq', cap_req)
    return jsonify({"success": True})


# input: json in format of {"email": "bob@email.com", "pubkey": "THISISAPUBKEY"}
# response: json in format of {success: true, "verification_nonce": "SOMENONCEHERE"}
# send an email with a special token to email address passed in
# adds the email to the emails table, pubkey email combo to the devices table
# idempotent function, will return success if user tries to register again
@app.route('/register', methods=['POST'])
def register():
    print(request.data)

    data = request.form.to_dict()
    if not RegisterRequest.is_valid(data):
        return jsonify({"success": False}), HTTPStatus.BAD_REQUEST

    reg_req = RegisterRequest(request.form)

    if not reg_req.insert():
        return jsonify({"success": False}), HTTPStatus.BAD_REQUEST

    return jsonify({"success": True})


@app.teardown_appcontext
def close_connection(exception):
    session_factory = getattr(app.config, 'session_factory', None)
    if session_factory is not None:
        session_factory.close_all_sessions()


def init_db():
    db.init_db()


if __name__ == "__main__":
    app.run()
