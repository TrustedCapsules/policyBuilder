import os
import json
import logging  # for debug
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from backend.server import app
from sqlalchemy.orm import sessionmaker

from sqlalchemy.engine import Engine  # for fk
from sqlalchemy import event  # ditto
from jsonschema import validate
from typing import Tuple


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record) -> None:
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


# an email can have 1..many devices
# a capsule can have 1..many capsule recipients

Base = sa.ext.declarative.declarative_base()  # need this to avoid making explicit tables


class Email(Base):
    __tablename__ = 'emails'
    email = sa.Column(sa.String, primary_key=True)
    devices = sa.orm.relationship('Device')

    def __repr__(self):
        return "<Email(email='%s', device='%s')>" % (
            self.email, self.devices)


class Device(Base):
    __tablename__ = 'devices'
    pubkey = sa.Column(sa.String, primary_key=True)
    email = sa.Column(sa.String, sa.ForeignKey(Email.email), nullable=False)
    nonce = sa.Column(sa.String, nullable=False)
    is_auth = sa.Column(sa.Boolean, nullable=False)

    def __repr__(self):
        return "<Device(pubkey='%s', email='%s', nonce='%s', is_auth='%s')>" % (
            self.pubkey, self.email, self.nonce, self.is_auth)


class Capsule(Base):
    __tablename__ = 'capsules'
    uuid = sa.Column(sa.String, primary_key=True)
    decrypt_key = sa.Column(sa.String, unique=True)
    recipients = sa.orm.relationship('CapsuleRecipient', back_populates='capsule')

    def __repr__(self):
        return "<Capsule(uuid='%s', decrypt_key='%s', recipients='%s')>" % (
            self.uuid, self.decrypt_key, self.recipients)


class CapsuleRecipient(Base):
    __tablename__ = 'capsule_recipients'
    __table_args__ = (sa.PrimaryKeyConstraint('uuid', 'email', name='capsule_recipients_pk'),)
    uuid = sa.Column(sa.String, sa.ForeignKey(Capsule.uuid), index=True, nullable=False)
    email = sa.Column(sa.String, nullable=False)
    capsule = sa.orm.relationship('Capsule', back_populates='recipients')

    def __repr__(self):
        return "<CapsuleRecipient(uuid='%s', email='%s', capsule='%s')>" % (
            self.uuid, self.email, self.capsule)


def get_engine() -> sa.engine:
    engine = getattr(app.config, 'engine', None)
    if engine is None:
        engine = app.config['engine'] = sa.create_engine('sqlite:///' + app.config['DATABASE'])
    return engine


def get_session() -> sa.orm.session.Session:
    SessionFactory = getattr(app.config, 'SessionFactory', None)
    if SessionFactory is None:
        SessionFactory = app.config['SessionFactory'] = sessionmaker()
        SessionFactory.configure(bind=get_engine())
    return SessionFactory()


def init_db() -> None:
    if app.testing:
        logging.basicConfig()
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
        if os.path.isfile(app.config['DATABASE']):
            os.unlink(app.config['DATABASE'])
    get_session()
    Base.metadata.create_all(get_engine())  # generate the tables


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


# expects
# returns an ok, nonce tuple
def register_device(json_str: str) -> Tuple[bool, str]:
    try:
        validate_register_device(json_str)
        return True, "NONCE"
    except:
        return False, ""


def validate_register_device(json_str: str):
    schema = {
        "type": "object",
        "properties": {
            "pubkey": {"type": "string"},
            "email": {"type": "string"},
        }
    }
    validate(instance=json.loads(json_str), schema=schema)


# expects
# returns an ok, nonce tuple
def gen_capsule(json_str: str) -> Tuple[bool, str]:
    try:
        validate_gen_request(json_str)
        return True, "NONCE"
    except:
        return False, ""


def validate_gen_request(json_str: str):
    schema = {
        "type": "object",
        "properties": {
            "file": {"type": "number"},
            "policy": {"type": "string"},
            "email1": {"type": "string"},
            "email2": {"type": "string"},
        }
    }

    validate(instance=json.loads(json_str), schema=schema)


@app.teardown_appcontext
def close_connection(exception):
    SessionFactory = getattr(app.config, 'SessionFactory', None)
    if SessionFactory is not None:
        SessionFactory.close_all_sessions()


if __name__ == "__main__":
    init_db()
    load_sample_data()
    session = get_session()
    our_user = session.query(Device)
    print(our_user)

# session.query.join(Address, User.id == Address.user_id)
