import os
import tempfile
import pytest
import sqlalchemy as sa
from backend import keyserver
from backend.db import Email, Device, Capsule, CapsuleRecipient, get_session


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


def load_sample_data() -> None:
    session = get_session()
    email1 = Email(email='c1r1@test.com')
    email2 = Email(email='c2r1@test.com')
    device1 = Device(pubkey='pubkeyNOAUTH', email=email1.email, nonce='nonceNOAUTH', is_auth=False)
    device2 = Device(pubkey='pubkeyAUTH', email=email2.email, nonce='nonceAUTH', is_auth=True)
    cap1 = Capsule(uuid="uuid1", decrypt_key="key1")
    cap2 = Capsule(uuid="uuid2", decrypt_key="key2")
    cap1recip1 = CapsuleRecipient(uuid=cap1.uuid, email=device1.email)
    cap1recip2 = CapsuleRecipient(uuid=cap1.uuid, email=device2.email)
    cap2recip1 = CapsuleRecipient(uuid=cap2.uuid, email=device1.email)
    session.add_all([email1, email2, device1, device2, cap1, cap2, cap1recip1, cap1recip2, cap2recip1])
    session.commit()


def test_query(client):
    with keyserver.app.app_context():
        load_sample_data()
        test_session = get_session()
        assert test_session.query(Email).count() == 2
        assert test_session.query(Device).count() == 2
        assert test_session.query(Capsule).count() == 2
        assert test_session.query(CapsuleRecipient).count() == 3
        # test_session.query.join(Address, User.id == Address.user_id)
