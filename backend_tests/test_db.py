import os
import tempfile

import pytest

from backend import server


@pytest.fixture
def client():
    db_fd, server.app.config['DATABASE'] = tempfile.mkstemp()
    server.app.config['TESTING'] = True
    client = server.app.test_client()

    with server.app.app_context():
        server.init_db()

    yield client

    os.close(db_fd)
    os.unlink(server.app.config['DATABASE'])
    assert False

def test_hello():
    assert True