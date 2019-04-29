import os
import tempfile

import pytest

from backend import keyserver, db


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
        test_session = db.get_session()
        assert test_session.query(db.Email).count() == 0
        assert test_session.query(db.Device).count() == 0
        test_session.close()
        resp = client.post('/register', json={"email": "bob@email.com",
                                              "pubkey": open("backend_tests/demo_rsakey.pub", "r").read()})

        test_session = db.get_session()
        assert resp.status_code == 200
        assert test_session.query(db.Email).count() == 1
        assert test_session.query(db.Device).count() == 1
        test_session.close()


def test_capsule_request(client):
    with keyserver.app.app_context():
        test_session = db.get_session()
        assert test_session.query(db.Capsule).count() == 0
        assert test_session.query(db.CapsuleRecipient).count() == 0
        test_session.close()

        resp = client.post('/capsule',
                           content_type='multipart/form-data',
                           data={"email1": "a@email.com",
                                 "email2": "b@email.com",
                                 "inviteRecipients": "true",
                                 "demo.lua": open("backend_tests/demo.lua", "rb")})

        assert resp.status_code == 200
        test_session = db.get_session()
        assert test_session.query(db.Capsule).count() == 1
        assert test_session.query(db.CapsuleRecipient).count() == 2
        test_session.close()
