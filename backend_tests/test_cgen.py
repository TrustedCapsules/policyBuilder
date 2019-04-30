import os
import tempfile

import pytest

import cgen
from backend import keyserver


@pytest.fixture
def client():
    db_fd, keyserver.app.config['DATABASE'] = tempfile.mkstemp()
    keyserver.app.config['TESTING'] = True
    keyserver.app.config['GENERATED_CAPSULES_PATH'] = 'backend_tests'
    client = keyserver.app.test_client()

    with keyserver.app.app_context():
        keyserver.init_db()

    yield client
    os.close(db_fd)
    os.unlink(keyserver.app.config['DATABASE'])


def test_get_capsule_uuid(client):
    with keyserver.app.app_context():
        assert cgen.get_capsule_uuid(
            'KEYSERVER_2019-04-29_17-30-09__0x1806.capsule') == '76f80b6050c34c88a7ac6b7d0999b38f'
