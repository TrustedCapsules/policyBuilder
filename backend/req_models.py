import base64
import uuid
from dataclasses import dataclass
from typing import Tuple, Dict

from Cryptodome.Random import get_random_bytes
from jsonschema import validate
from jsonschema.exceptions import FormatError, ValidationError

import crypto
import db


@dataclass
class RegisterRequest:
    email: str
    pubkey: str

    def __init__(self, data: Dict[str, str]) -> None:
        self.email = data['email']
        self.pubkey = data['pubkey']

    @staticmethod
    def is_valid(req: Dict[str, str]) -> bool:
        schema = {
            "type": "object",
            "properties": {
                "email": {"type": "string", "format": "email"},
                "pubkey": {"type": "string"},
            }
        }

        try:
            validate(instance=req, schema=schema)
            return True
        except FormatError:
            print('format err')
            return False
        except ValidationError:
            print('validation err')
            return False

    # returns an encrypted nonce and success bool
    def insert(self) -> Tuple[str, bool]:
        nonce = base64.urlsafe_b64encode(get_random_bytes(16))
        session = db.get_session()
        email = db.Email(email=self.email)
        device = db.Device(pubkey=self.pubkey, email=self.email, nonce=nonce, is_auth=False)
        session.add_all([email, device])
        try:
            session.commit()
            encrypted_nonce = str(crypto.encrypt_rsa(nonce, self.pubkey))
            return encrypted_nonce, True
        except Exception as e:
            print(e)
            session.rollback()
            return "", False


@dataclass
class VerifyRequest:
    email: str
    pubkey: str
    nonce: str

    def __init__(self, data: Dict[str, str]) -> None:
        self.email = data['email']
        self.pubkey = data['pubkey']
        self.nonce = data['nonce']

    @staticmethod
    def is_valid(req: Dict[str, str]) -> bool:
        schema = {
            "type": "object",
            "properties": {
                "email": {"type": "string", "format": "email"},
                "pubkey": {"type": "string"},
                "nonce": {"type": "string"},
            }
        }

        try:
            validate(instance=req, schema=schema)
            return True
        except FormatError:
            print('format err')
            return False
        except ValidationError:
            print('validation err')
            return False

    #TODO: make work
    def insert(self) -> Tuple[str, bool]:
        session = db.get_session()
        email = db.Email(email=self.email)
        device = db.Device(pubkey=self.pubkey, email=self.email, nonce=nonce, is_auth=False)
        session.add_all([email, device])
        try:
            session.commit()
            encrypted_nonce = str(crypto.encrypt_rsa(nonce, self.pubkey))
            return encrypted_nonce, True
        except Exception as e:
            print(e)
            session.rollback()
            return "", False


@dataclass
class CapsuleRequest:
    email1: str
    email2: str
    policy_filename: str
    invite_recipients: bool

    def __init__(self, data: Dict[str, str], policy_filename: str) -> None:
        self.email1 = data['email1']
        self.email2 = data['email2']
        self.policy_filename = policy_filename
        self.invite_recipients = (data['inviteRecipients'] == 'true')

    @staticmethod
    def is_valid(req: Dict[str, str]) -> bool:
        schema = {
            "type": "object",
            "properties": {
                "email1": {"type": "string", "format": "email"},
                "email2": {"type": "string", "format": "email"},
                "inviteRecipients": {
                    "type": "string",
                    "pattern": "^(true)$|^(false)$"
                },  # should be bool, html makes it a string
            }
        }

        try:
            validate(instance=req, schema=schema)
            return True
        except FormatError:
            print('format err')
            return False
        except ValidationError:
            print('validation err')
            return False

    # returns a file path to a generated capsule, and success bool
    def insert(self) -> Tuple[str, bool]:
        session = db.get_session()
        cap_uuid = uuid.uuid4().hex
        recip1 = db.CapsuleRecipient(uuid=cap_uuid, email=self.email1)
        recip2 = db.CapsuleRecipient(uuid=cap_uuid, email=self.email2)
        decrypt_key = get_random_bytes(16).hex()
        cap = db.Capsule(uuid=cap_uuid, decrypt_key=decrypt_key, recipients=[recip1, recip2])
        session.add_all([cap, recip1, recip2])

        # TODO: call cgen code here
        try:
            session.commit()
            return "SOME GENERATED CAPSULE FILENAME", True
        except Exception as e:
            print(e)
            session.rollback()
            return "", False
