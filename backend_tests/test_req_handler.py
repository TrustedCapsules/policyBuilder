import os
import pytest
import tempfile
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

        resp = client.post('/register', json={"email": "bob@email.com",
                                              "pubkey": "THISISAPUBKEY"})

        assert resp.status_code == 200
        assert test_session.query(db.Email).count() == 1
        assert test_session.query(db.Device).count() == 1
        assert db.Email
    # data = json.loads(resp.data)
    # self.assert_equal(data['username'], my_user.username)


def test_capsule_request():
    # with keyserver.app.test_client() as c:
    #     resp = c.post('/capsule',
    #                   content_type='multipart/form-data',
    #                   data={"email": "bob@email.com", "pubkey": "THISISAPUBKEY"})
    #     print('respdata', resp.data)
    #     assert resp.status_code == 200
    #     # data = json.loads(resp.data)
    #     # self.assert_equal(data['username'], my_user.username)
    pass
