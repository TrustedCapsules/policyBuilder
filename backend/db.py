import os
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from flask import g
from backend.server import app
from sqlalchemy.orm import sessionmaker
SessionFactory = sessionmaker()
Base = db.ext.declarative.declarative_base()
DATABASE = 'db.sqlite'


class Device(Base):
    __tablename__ = 'devices'
    pubkey = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, index=True, nullable=False)
    nonce = db.Column(db.String, nullable=False)
    is_auth = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return "<Device(pubkey='%s', email='%s', nonce='%s', is_auth=%s)>" % (
            self.pubkey, self.email, self.nonce, self.is_auth)


class Capsule(Base):
    __tablename__ = 'capsules'
    uuid = db.Column(db.String, primary_key=True)
    decrypt_key = db.Column(db.String, unique=True)

    def __repr__(self):
        return "<Capsule(uuid='%s', decrypt_key='%s')>" % (
            self.uuid, self.decrypt_key)


# can have multiple emails per capsule
class CapsuleRecipient(Base):
    __tablename__ = 'capsule_recipients'
    __table_args__ = (db.PrimaryKeyConstraint('uuid', 'email', name='capsule_recipients_pk'),)
    uuid = db.Column(db.String, db.ForeignKey(Capsule.uuid), index=True, nullable=False)
    email = db.Column(db.String)

    def __repr__(self):
        return "<CapsuleRecipient(uuid='%s', email='%s')>" % (
            self.uuid, self.email)


def init_db(persist: bool = False) -> None:
    if not persist and os.path.isfile(DATABASE):
        os.unlink(DATABASE)
    engine = db.create_engine('sqlite:///' + DATABASE)
    # for tablename in [Capsule.__tablename__, CapsuleRecipient.__tablename__, Device.__tablename__]:
    #     if not engine.dialect.has_table(engine, Device.__tablename__):  # If table don't exist, Create.
    Base.metadata.create_all(engine)


def load_sample_data()->None:



def get_db():
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
#
# a = Device()
# print(a)
# import inspect
# print(inspect.signature(a.__init__))
