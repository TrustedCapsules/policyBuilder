import tempfile
import pytest
from sqlalchemy import exc
from backend import server, db
from backend.db import *


@pytest.fixture
def client():
    db_fd, server.app.config['DATABASE'] = tempfile.mkstemp()
    server.app.config['TESTING'] = True
    client = server.app.test_client()

    with server.app.app_context():
        db.init_db()

    yield client
    os.close(db_fd)
    os.unlink(server.app.config['DATABASE'])


def test_fk_raises_exception():
    session = get_session()
    email1 = Email(email="1@test.com")
    device1 = Device(pubkey='pubkeyNOAUTH', email='2@test.com', nonce='nonceNOAUTH', is_auth=False)
    session.add_all([email1, device1])
    with pytest.raises(exc.OperationalError):
        session.commit()
