import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from passlib.hash import bcrypt


class UserPassword:
    def __init__(self) -> None:
        # Initialize bcrypt
        self.pwd_context = bcrypt.using(rounds=12)

    def verify_hash(self, plain_phrase, hashed_phrase):
        return self.pwd_context.verify(plain_phrase, hashed_phrase)

    def get_hash(self, phrase):
        return self.pwd_context.hash(phrase)


class SecretHash:
    def __init__(self, passphrase: str) -> None:
        encoding_engine = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=bytes(passphrase, encoding='utf-8'),
            iterations=390000,
        )
        self.passphrase_fernet = base64.urlsafe_b64encode(encoding_engine.derive(bytes(passphrase, encoding='utf-8')))
        self.engine = Fernet(self.passphrase_fernet)

    def hash_secret(self, secret: str):
        return self.engine.encrypt(bytes(secret, encoding='utf-8'))

    def get_secret(self, hashed_secret: str):
        return self.engine.decrypt(hashed_secret)
