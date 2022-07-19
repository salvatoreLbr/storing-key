from src.storing_key import get_db
from src.storing_key.cmd import *
from src.storing_key.db.crud import get_user, get_secret


def test_create_delete_user():
    username = 'prova'
    password = 'hahaha23'
    # check if user already exist
    if get_user(db=get_db(), username=username) is not None:
        delete_user_from_db(username, password, db=get_db())
    create_new_user(username, password, db=get_db())

def test_create_delete_secret():
    # Set username and password
    username = 'prova'
    password = 'hahaha23'

    # Add one secret
    key = 'website'
    secret = 'website$$2'
    passphrase = 'useThisPassPhrase'
    # check if secret already exist
    if get_secret(db=get_db(), key_name=key) is not None:
        delete_secret_from_db(username, password, key, db=get_db())
    create_new_secret(username, password, key, secret, passphrase, db=get_db())

    # Add another secret
    key = 'website2'
    secret = 'website2'
    passphrase = 'useThisPassPhrase_2'
    # check if secret already exist
    if get_secret(db=get_db(), key_name=key) is not None:
        delete_secret_from_db(username, password, key, db=get_db())
    create_new_secret(username, password, key, secret, passphrase, db=get_db())
    

def test_list_secret():
    username = 'prova'
    password = 'hahaha23'
    secrets_list = list_secrets(username, password, db=get_db())
    
    assert 'website' in secrets_list
    assert 'website2' in secrets_list


def test_secret_element():
    username = 'prova'
    password = 'hahaha23'
    key = 'website'
    passphrase = 'useThisPassPhrase'
    assert get_secret_from_db(username, password, key, passphrase, db=get_db()) == 'website$$2'
