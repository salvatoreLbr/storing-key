import base64
import inspect
from typing import Type

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from fastapi import Form
from passlib.hash import bcrypt
from pydantic import BaseModel
from pydantic.fields import ModelField


def as_form(cls: Type[BaseModel]):
    new_parameters = []

    for field_name, model_field in cls.__fields__.items():
        model_field: ModelField  # type: ignore

        if not model_field.required:
            new_parameters.append(
                inspect.Parameter(
                    model_field.alias,
                    inspect.Parameter.POSITIONAL_ONLY,
                    default=Form(model_field.default),
                    annotation=model_field.outer_type_,
                )
            )
        else:
            new_parameters.append(
                inspect.Parameter(
                    model_field.alias,
                    inspect.Parameter.POSITIONAL_ONLY,
                    default=Form(...),
                    annotation=model_field.outer_type_,
                )
            )

    async def as_form_func(**data):
        return cls(**data)

    sig = inspect.signature(as_form_func)
    sig = sig.replace(parameters=new_parameters)
    as_form_func.__signature__ = sig  # type: ignore
    setattr(cls, "as_form", as_form_func)
    return cls


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
            salt=bytes(passphrase, encoding="utf-8"),
            iterations=390000,
        )
        self.passphrase_fernet = base64.urlsafe_b64encode(
            encoding_engine.derive(bytes(passphrase, encoding="utf-8"))
        )
        self.engine = Fernet(self.passphrase_fernet)

    def hash_secret(self, secret: str):
        return self.engine.encrypt(bytes(secret, encoding="utf-8"))

    def get_secret(self, hashed_secret: str):
        return self.engine.decrypt(hashed_secret)


@as_form
class RegistrationForm(BaseModel):
    username: str
    password: str


@as_form
class AddKeyForm(RegistrationForm):
    key: str
    secret: str
    passphrase: str


@as_form
class DeleteKeyForm(RegistrationForm):
    key: str


@as_form
class ShowKeyForm(RegistrationForm):
    key: str
    passphrase: str
