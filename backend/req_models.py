import db
import uuid
from dataclasses import dataclass
from jsonschema import validate
from jsonschema.exceptions import FormatError, ValidationError
from typing import Tuple, Dict


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

    # returns a nonce and success bool
    def insert(self) -> Tuple[str, bool]:
        nonce = str(uuid.uuid4())
        print('inserting', self)
        session = db.get_session()
        email = db.Email(email=self.email)
        device = db.Device(pubkey=self.pubkey, email=self.email, nonce=nonce, is_auth=False)
        session.add_all([email, device])
        return nonce, True


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

    # returns a capsule file path, and success bool
    def insert(self) -> Tuple[str, bool]:
        print('inserting', self)
        return "SOME GENERATED CAPSULE FILENAME", True
