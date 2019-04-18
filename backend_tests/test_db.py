import os
import tempfile
import pytest
import sqlalchemy as sa
from backend import keyserver
from backend.db import Email, Device, get_session


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


def test_fk_raises_exception(client):
    with keyserver.app.app_context():
        session = get_session()
        email1 = Email(email="1@test.com")
        device1 = Device(pubkey='pubkeyNOAUTH', email='2@test.com', nonce='nonceNOAUTH', is_auth=False)
        session.add_all([email1, device1])
        with pytest.raises(sa.exc.IntegrityError):  # fk check fails
            session.commit()
