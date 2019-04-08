import os
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from backend.server import app
from sqlalchemy.orm import sessionmaker


def enable_debug():
    import logging
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


enable_debug()

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

Base = db.ext.declarative.declarative_base()


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


def get_engine():
    engine = getattr(app.config, 'engine', None)
    if engine is None:
        engine = app.config['engine'] = db.create_engine('sqlite:///' + app.config['DATABASE'])
    return engine


def get_session():
    SessionFactory = getattr(app.config, 'SessionFactory', None)
    if SessionFactory is None:
        SessionFactory = app.config['SessionFactory'] = sessionmaker()
        SessionFactory.configure(bind=get_engine())
    return SessionFactory()


def init_db(persist: bool = False) -> None:
    if not persist and os.path.isfile(app.config['DATABASE']):
        os.unlink(app.config['DATABASE'])
    session = get_session()
    Base.metadata.create_all(get_engine())


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


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, app.config['DATABASE'], None)
    if db is not None:
        db.close()


if __name__ == "__main__":
    init_db()
    load_sample_data()
    session = get_session()
    our_user = session.query(Device)
    print(our_user)

# session.query.join(Address, User.id == Address.user_id)

