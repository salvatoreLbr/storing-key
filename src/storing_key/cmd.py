from typing import Optional

from cryptography.fernet import InvalidToken
from sqlalchemy.orm import Session

from src.storing_key.db.crud import (
    create_key,
    create_user,
    delete_secret,
    delete_user,
    get_all_keys,
    get_secret,
    get_user,
)
from src.storing_key.utils.authorization import SecretHash, UserPassword


def create_new_user(
    username: str, password: str, db: Session, print_output: Optional[bool] = False
):
    # init class
    user_psw = UserPassword()
    # write user in table
    user_info = {"username": username, "hashed_password": user_psw.get_hash(password)}
    create_user(db, user_info)
    if print_output:
        print("#- Username {} created".format(username))


def create_new_secret(
    username: str,
    password: str,
    key: str,
    secret: str,
    passphrase: str,
    db: Session,
    print_output: Optional[bool] = False,
):
    # Get user_info
    user_info = get_user(db, username=username)
    if user_info is not None:
        # init class
        user_psw = UserPassword()
        # check password
        check_psw = user_psw.verify_hash(
            plain_phrase=password, hashed_phrase=user_info.hashed_password
        )
        if check_psw:
            # create key-secret
            secret_hash = SecretHash(passphrase=passphrase)
            hashed_secret = secret_hash.hash_secret(secret)
            key_info = {
                "user_id": user_info.id,
                "key_name": key,
                "hashed_secret": hashed_secret,
            }
            create_key(db, key_info)
            if print_output:
                print("#- Secret for key {} added".format(key))
            return "SecretAdded"
        else:
            if print_output:
                print("!! Wrong password")
            return "WrongPassword"
    else:
        if print_output:
            print("#- User {} not exist".format(username))
        return "UserNotExist"


def list_secrets(
    username: str, password: str, db: Session, print_output: Optional[bool] = False
):
    # Get user_info
    user_info = get_user(db, username=username)
    if user_info is not None:
        # init class
        user_psw = UserPassword()
        # check password
        check_psw = user_psw.verify_hash(
            plain_phrase=password, hashed_phrase=user_info.hashed_password
        )
        if check_psw:
            if print_output:
                print("#- Keys for user: {}".format(username))
            obj_keys = get_all_keys(db, user_id=user_info.id)
            keys_list = []
            for obj in obj_keys:
                if print_output:
                    print("##-- Key: {}".format(obj.key_name))
                keys_list.append(obj.key_name)
        else:
            if print_output:
                print("!! Wrong password")
            return [], "WrongPassword"
    else:
        if print_output:
            print("#- User {} not exist".format(username))
        return [], "UserNotExist"

    return keys_list, "AllSecrets"


def get_secret_from_db(
    username: str,
    password: str,
    key: str,
    passphrase: str,
    db: Session,
    print_output: Optional[bool] = False,
):
    # Get user_info
    user_info = get_user(db, username=username)
    if user_info is not None:
        # init class
        user_psw = UserPassword()
        # check password
        check_psw = user_psw.verify_hash(
            plain_phrase=password, hashed_phrase=user_info.hashed_password
        )
        if check_psw:
            # get secret from db
            secret_info = get_secret(db, key_name=key)
            if secret_info is not None:
                hashed_secret = secret_info.hashed_secret
                secret_hash = SecretHash(passphrase=passphrase)
                try:
                    clean_secret = str(secret_hash.get_secret(hashed_secret), "utf-8")
                except InvalidToken:
                    return [key, ""], "WrongPassphrase"
                if print_output:
                    print("#- Key: {} - Secret: {}".format(key, clean_secret))
                return [key, clean_secret], "GetSecret"
            else:
                if print_output:
                    print("#- Key: {} not exist".format(key))
                return [key, ""], "KeyNotExist"
        else:
            if print_output:
                print("!! Wrong password")
            return [key, ""], "WrongPassword"
    else:
        if print_output:
            print("#- User {} not exist".format(username))
        return [key, ""], "UserNotExist"


def delete_user_from_db(
    username: str, password: str, db: Session, print_output: Optional[bool] = False
):
    # Get user_info
    user_info = get_user(db, username=username)
    if user_info is not None:
        # init class
        user_psw = UserPassword()
        # check password
        check_psw = user_psw.verify_hash(
            plain_phrase=password, hashed_phrase=user_info.hashed_password
        )
        if check_psw:
            # delete user
            delete_user(db, username)
            if print_output:
                print("#- User {} deleted".format(username))
        else:
            if print_output:
                print("!! Wrong password")
    else:
        if print_output:
            print("#- User {} not exist".format(username))


def delete_secret_from_db(
    username: str,
    password: str,
    key: str,
    db: Session,
    print_output: Optional[bool] = False,
):
    # Get user_info
    user_info = get_user(db, username=username)
    if user_info is not None:
        # init class
        user_psw = UserPassword()
        # check password
        check_psw = user_psw.verify_hash(
            plain_phrase=password, hashed_phrase=user_info.hashed_password
        )
        if check_psw:
            # delete secret
            delete_secret(db, key)
            if print_output:
                print("#- Key {} deleted".format(key))
            return "SecretDeleted"
        else:
            if print_output:
                print("!! Wrong password")
            return "WrongPassword"
    else:
        if print_output:
            print("#- User {} not exist".format(username))
        return "UserNotExist"
