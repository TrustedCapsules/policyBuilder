import os
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from flask import g
from backend.server import app
from sqlalchemy.orm import sessionmaker


def enable_debug():
    import logging
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


enable_debug()

SessionFactory = sessionmaker()
Base = db.ext.declarative.declarative_base()
DATABASE = 'db.sqlite'

from sqlalchemy.engine import Engine
from sqlalchemy import event


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


# an email can have 1..many devices
# a capsule can have 1..many capsule recipients
# a


class Email(Base):
    __tablename__ = 'emails'
    email = db.Column(db.String, primary_key=True)
    devices = db.orm.relationship('Device')

    def __repr__(self):
        return "<Email(email='%s', device='%s')>" % (
            self.email, self.devices)


class Device(Base):
    __tablename__ = 'devices'
    pubkey = db.Column(db.String, primary_key=True)
    email = db.Column(db.String, db.ForeignKey(Email.email), nullable=False)
    nonce = db.Column(db.String, nullable=False)
    is_auth = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return "<Device(pubkey='%s', email='%s', nonce='%s', is_auth='%s')>" % (
            self.pubkey, self.email, self.nonce, self.is_auth)


class Capsule(Base):
    __tablename__ = 'capsules'
    uuid = db.Column(db.String, primary_key=True)
    decrypt_key = db.Column(db.String, unique=True)
    recipients = db.orm.relationship('CapsuleRecipient', back_populates='capsule')

    def __repr__(self):
        return "<Capsule(uuid='%s', decrypt_key='%s', recipients='%s')>" % (
            self.uuid, self.decrypt_key, self.recipients)


class CapsuleRecipient(Base):
    __tablename__ = 'capsule_recipients'
    __table_args__ = (db.PrimaryKeyConstraint('uuid', 'email', name='capsule_recipients_pk'),)
    uuid = db.Column(db.String, db.ForeignKey(Capsule.uuid), index=True, nullable=False)
    email = db.Column(db.String, db.ForeignKey(Email.email), nullable=False)
    capsule = db.orm.relationship('Capsule', back_populates='recipients')

    def __repr__(self):
        return "<CapsuleRecipient(uuid='%s', email='%s', capsule='%s')>" % (
            self.uuid, self.email, self.capsule)


def init_db(persist: bool = False) -> None:
    if not persist and os.path.isfile(DATABASE):
        os.unlink(DATABASE)
    engine = db.create_engine('sqlite:///' + DATABASE)
    SessionFactory.configure(bind=engine)
    # for tablename in [Capsule.__tablename__, CapsuleRecipient.__tablename__, Device.__tablename__]:
    #     if not engine.dialect.has_table(engine, Device.__tablename__):  # If table don't exist, Create.
    Base.metadata.create_all(engine)


def load_sample_data() -> None:
    session = SessionFactory()
    email1 = Email(email='c1r1@test.com')
    email2 = Email(email='c2r1@test.com')
    device1 = Device(pubkey='pubkeyNOAUTH', email=email1.email, nonce='nonceNOAUTH', is_auth=False)
    device2 = Device(pubkey='pubkeyAUTH', email=email2.email, nonce='nonceAUTH', is_auth=True)
    cap1 = Capsule(uuid="uuid1", decrypt_key="key1")
    cap2 = Capsule(uuid="uuid2", decrypt_key="key2")
    cap1recip1 = CapsuleRecipient(uuid="uuid1", email=device1.email)
    cap1recip2 = CapsuleRecipient(uuid="uuid1", email=device2.email)
    cap2recip1 = CapsuleRecipient(uuid="uuid2", email=device1.email)
    session.add_all([email1, email2, device1, device2, cap1, cap2, cap1recip1, cap1recip2, cap2recip1])
    session.commit()


def get_session():
    db = g._database
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


init_db()
load_sample_data()
session = SessionFactory()
our_user = session.query(Device)
print(our_user)

# session.add(CapsuleRecipient(uuid="uuid2", email="99999999@test.com"))
# session.commit()
print(session)
# session.query.join(Address, User.id == Address.user_id)
#
# a = Device()
# print(a)
# import inspect
# print(inspect.signature(a.__init__))
