import tempfile
import pytest
import os
from backend import keyserver
from backend.req_parser import RegisterRequest, CapsuleRequest


@pytest.fixture
def client():
    db_fd, keyserver.app.config['DATABASE'] = tempfile.mkstemp()
    keyserver.app.config['TESTING'] = True
    client = keyserver.app.test_client()

    with keyserver.app.app_context():
        keyserver.init_db()

    yield client
    os.close(db_fd)
    os.unlink(keyserver.app.config['DATABASE'])


def test_capsule_request(client):
    form_data = {"email1": "a@email.com",
                 "email2": "b@email.com",
                 "inviteRecipients": "true"}
    assert CapsuleRequest.is_valid(form_data)
    cap_req = CapsuleRequest(form_data, "A FILEPATH HERE")
    capsule_filename, ok = cap_req.insert()
    assert capsule_filename != '' and ok


def test_register_request(client):
    form_data = {"email": "bob@email.com", "pubkey": "THISISAPUBKEY"}
    assert RegisterRequest.is_valid(form_data)
    reg_req = RegisterRequest(form_data)
    nonce, ok = reg_req.insert()
    assert nonce != '' and ok
