import req_handler
from flask import Flask, request, send_from_directory, send_file
from db import init_db as init_db1

app = Flask(__name__)
app.config['DATABASE'] = 'db.sqlite'
app.config['TESTING'] = True


@app.route('/dist/<path:path>')
def send_js(path):
    return send_from_directory('dist', path)


@app.route("/")
def home():
    return send_file('html/index.html')


# input: application/json request in format of {"email": "bob@email.com", "pubkey": "THISISAPUBKEY"}
# response: json in format of {success: true, "verification_nonce": "SOMENONCEHERE"}
# send an email with a special token to email address passed in
# adds the email to the emails table, pubkey email combo to the devices table
# does not allow reregistration of email TODO: ask ivan
@app.route('/register', methods=['POST'])
def register():
    return req_handler.register_request(request)


# input: application/json request in format of {"email": "bob@email.com", "pubkey": "THISISAPUBKEY"}
# response: json in format of {success: true, "verification_nonce": "SOMENONCEHERE"}
# send an email with a special token to email address passed in
# adds the email to the emails table, pubkey email combo to the devices table
# idempotent function, will return success if user tries to register again
@app.route('/capsule', methods=['POST'])
def capsule():
    return req_handler.capsule_request(request)


@app.teardown_appcontext
def close_connection(exception):
    session_factory = getattr(app.config, 'session_factory', None)
    if session_factory is not None:
        session_factory.close_all_sessions()


@app.before_first_request
def init_db():
    init_db1()


if __name__ == "__main__":
    app.run()
