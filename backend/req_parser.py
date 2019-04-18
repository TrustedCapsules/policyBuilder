import uuid
from dataclasses import dataclass
from typing import Tuple, Dict
from jsonschema import validate
from jsonschema.exceptions import FormatError, ValidationError


@dataclass
class CapsuleRequest:
    policy_filename: str
    email1: str
    email2: str
    invite_recipients: bool

    def __init__(self, data: Dict[str, str], policy_filename: str) -> None:
        self.policy_filename = policy_filename
        self.email1 = data['email1']
        self.email2 = data['email2']
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


@dataclass
class RegisterRequest:
    pubkey: str
    email: str

    def __init__(self, data: Dict[str, str]) -> None:
        self.pubkey = data['pubkey']
        self.email = data['email']

    @staticmethod
    def is_valid(req: Dict[str, str]) -> bool:
        schema = {
            "type": "object",
            "properties": {
                "pubkey": {"type": "string"},
                "email": {"type": "string", "format": "email"},
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
        return nonce, True
