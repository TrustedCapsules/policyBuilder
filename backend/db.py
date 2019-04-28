import logging  # for debug
import os

import sqlalchemy as sa
from flask import g, current_app
from sqlalchemy import event  # ditto
from sqlalchemy.engine import Engine  # for fk
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# an email can have 1..many devices
# a capsule can have 1..many capsule recipients

Base = sa.ext.declarative.declarative_base()  # need this to avoid making explicit tables


class Email(Base):
    __tablename__ = 'emails'
    email = sa.Column(sa.String, primary_key=True)
    devices = sa.orm.relationship('Device')

    def __repr__(self):
        return "<Email(email='%s', devices='%s')>" % (
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
    with current_app.app_context():
        engine = g.get('engine', None)
        if engine is None:
            engine = g.engine = sa.create_engine('sqlite:///' + current_app.config['DATABASE'])
        return engine


def get_session() -> sa.orm.session.Session:
    with current_app.app_context():
        session_factory = g.get('session_factory', None)
        if session_factory is None:
            session_factory = g.session_factory = sessionmaker()
            session_factory.configure(bind=get_engine())
        return session_factory()


def init_db() -> None:
    with current_app.app_context():
        if current_app.config['TESTING']:
            logging.basicConfig()
            logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
            if os.path.isfile(current_app.config['DATABASE']):
                os.unlink(current_app.config['DATABASE'])
        get_session()
        Base.metadata.create_all(get_engine())  # generate the tables


# forces fk to work (default is off)
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record) -> None:
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
