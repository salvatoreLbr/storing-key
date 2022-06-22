import click

from src.storing_key import get_db
from src.storing_key.cmd import (create_new_secret, create_new_user,
                                 delete_secret_from_db, delete_user_from_db,
                                 get_secret_from_db, list_secrets)


@click.group()
def storing_key():
    """CLI group for storing secret"""


@storing_key.command("create_user")
@click.argument("username")
@click.argument("password")
def create_user(username: str, password: str):
    """Function for creating an user

    Args: \n
    - username \n
    - password
    """
    create_new_user(username, password, db=get_db())


@storing_key.command("add_secret")
@click.argument("username")
@click.argument("password")
@click.argument("key")
@click.argument("secret")
@click.argument("passphrase")
def add_secret(username: str, password: str, key: str, secret: str, passphrase: str):
    """Function for adding a new secret

    Args: \n
    - username \n
    - password \n
    - key \n
    - secret \n
    - passphrase
    """
    create_new_secret(username, password, key, secret, passphrase, db=get_db())


@storing_key.command("list_secret")
@click.argument("username")
@click.argument("password")
def list_secret_cli(username: str, password: str):
    """Function for listing secrets about an user

    Args: \n
    - username \n
    - password
    """
    list_secrets(username, password, db=get_db())


@storing_key.command("get_secret")
@click.argument("username")
@click.argument("password")
@click.argument("key")
@click.argument("passphrase")
def get_secret(username: str, password: str, key: str, passphrase: str):
    """Function for getting a secret

    Args: \n
    - username \n
    - password \n
    - key \n
    - passphrase
    """
    get_secret_from_db(username, password, key, passphrase, db=get_db())


@storing_key.command("remove_secret")
@click.argument("username")
@click.argument("password")
@click.argument("key")
def delete_secret(username: str, password: str, key: str):
    """Function for deleting a secret

    Args: \n
    - username \n
    - password \n
    - key
    """
    delete_secret_from_db(username, password, key, db=get_db())


@storing_key.command("delete_user")
@click.argument("username")
@click.argument("password")
def delete_user(username: str, password: str):
    """Function for deleting an user

    Args: \n
    - username \n
    - password
    """
    delete_user_from_db(username, password, db=get_db())
