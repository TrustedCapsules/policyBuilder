import os
import tempfile

import pytest

import crypto
from backend import keyserver
from backend.req_models import RegisterRequest, VerifyRequest, CapsuleRequest


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


def test_register_request(client):
    with keyserver.app.app_context():
        form_data = {"email": "a@email.com",
                     "pubkey": open("demo_rsakey.pub", "r").read()}
        assert RegisterRequest.is_valid(form_data)
        reg_req = RegisterRequest(form_data)
        nonce, ok = reg_req.insert()
        assert len(nonce) > 0 and ok


def test_verify_request(client):
    with keyserver.app.app_context():
        reg_form_data = {"email": "a@email.com",
                         "pubkey": open("demo_rsakey.pub", "r").read()}
        reg_req = RegisterRequest(reg_form_data)
        hex_enc_nonce, ok = reg_req.insert()
        assert len(hex_enc_nonce) > 0 and ok

        privkey = open("demo_rsakey", "r").read()
        verify_form_data = {"email": "a@email.com",
                            "pubkey": open("demo_rsakey.pub", "r").read(),
                            "nonce": crypto.decrypt_rsa(bytes.fromhex(hex_enc_nonce), privkey).hex()}
        assert VerifyRequest.is_valid(verify_form_data)
        verify_req = VerifyRequest(verify_form_data)
        assert verify_req.insert()


def test_capsule_request(client):
    with keyserver.app.app_context():
        form_data = {"email1": "a@email.com",
                     "email2": "b@email.com",
                     "inviteRecipients": "true"}
        assert CapsuleRequest.is_valid(form_data)
        cap_req = CapsuleRequest(form_data, "A FILEPATH HERE")
        capsule_filename, ok = cap_req.insert()

        assert capsule_filename != '' and ok
