import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base


class Device(db.ext.declarative.declarative_base()):
    pubkey = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    nonce = db.Column(db.String)
    is_auth = db.Column(db.Boolean)

    __tablename__ = 'devices'

    def __repr__(self):
        return "<Device(pubkey='%s', email='%s', nonce='%s', is_auth=%s)>" % (
            self.pubkey, self.email, self.nonce, self.is_auth)


# engine = db.create_engine('sqlite:///db.sqlite')
# connection = engine.connect()
# metadata = db.MetaData()
# census = db.Table('census', metadata, autoload=True, autoload_with=engine)
#
# print(census.columns.keys())

a = Device()
print(a)
# import inspect
# print(inspect.signature(a.__init__))
