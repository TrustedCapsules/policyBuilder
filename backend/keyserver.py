import os

from flask import Flask, request, send_from_directory, send_file

import db
import req_handler

app = Flask(__name__)
app.config['DATABASE'] = 'db.sqlite'
app.config['TESTING'] = True  # FIXME make false
app.config['CGEN_PATH'] = 'backend'
app.config['CAPSULE_TEMP_WORK_PATH'] = '/tmp/keyserver'
app.config['GENERATED_CAPSULES_PATH'] = './generated_capsules'
app.config['UPLOADED_LUA_PATH'] = 'uploads'


@app.route('/dist/<path:path>')
def send_js(path):
    return send_from_directory('dist', path)


@app.route("/")
def home():
    return send_file('../html/index.html')


# input: application/json request in format of {"email": "bob@email.com", "pubkey": "EXAMPLE_PUBKEY"}
# response: json in format of {success: true, "verification_nonce": "ENC_NONCE_IN_HEX"}
# send an email with a special token to email address passed in
# adds the email to the emails table, pubkey email combo to the devices table
# idempotent
@app.route('/register', methods=['POST'])
def register():
    return req_handler.register_request(request)


# input: application/json of {"email": "a@a.com", "pubkey": "EXAMPLE_PUBKEY", "nonce": "DECRYPTED_NONCE_IN_HEX"}
# response: json in format of {success: true, "msg": ""}
@app.route('/verify', methods=['POST'])
def verify():
    return req_handler.verify_request(request)


# input: multipart/form request in format of
# {"email1": "a@a.com", "email2": "b@b.com", "inviteRecipients": "true", "file.lua": "contents"}
# response: json in format of {success: true, "url": "SERVER_IP:PORT/capsules/capsule1.cap"}
# sends an email with invitation
@app.route('/capsule', methods=['POST'])
def capsule():
    return req_handler.capsule_request(request)


# input: multipart/form request in format of
# {"uuid": "32CHAR_HEX_UUID", "pubkey": "EXAMPLE_PUBKEY"}
# response: json in format of {success: true, "key": "DECRYPT_KEY"}
@app.route('/decrypt', methods=['POST'])
def decrypt():
    return req_handler.decrypt_request(request)


@app.teardown_appcontext
def close_connection(exception):
    session_factory = getattr(app.config, 'session_factory', None)
    if session_factory is not None:
        session_factory.close_all_sessions()


@app.before_first_request
def init_db():
    os.makedirs(app.config['CAPSULE_TEMP_WORK_PATH'], exist_ok=True)
    db.init_db()


if __name__ == "__main__":
    app.run()
