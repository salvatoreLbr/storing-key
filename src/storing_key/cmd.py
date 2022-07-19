from sqlalchemy.orm import Session

from src.storing_key.db.crud import (create_key, create_user, delete_secret,
                                     delete_user, get_all_keys, get_secret,
                                     get_user)
from src.storing_key.utils.authorization import SecretHash, UserPassword


def create_new_user(username: str, password: str, db: Session):
    # init class
    user_psw = UserPassword()
    # write user in table
    user_info = {"username": username, "hashed_password": user_psw.get_hash(password)}
    create_user(db, user_info)
    print("#- Username {} created".format(username))


def create_new_secret(
    username: str, password: str, key: str, secret: str, passphrase: str, db: Session
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
            print("#- Secret for key {} added".format(key))
        else:
            print("!! Wrong password")
    else:
        print("#- User {} not exist".format(username))


def list_secrets(username: str, password: str, db: Session):
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
            print("#- Keys for user: {}".format(username))
            obj_keys = get_all_keys(db, user_id=user_info.id)
            keys_list = []
            for obj in obj_keys:
                print("##-- Key: {}".format(obj.key_name))
                keys_list.append(obj.key_name)
        else:
            print("!! Wrong password")
            keys_list = []
    else:
        print("#- User {} not exist".format(username))

    return keys_list


def get_secret_from_db(
    username: str, password: str, key: str, passphrase: str, db: Session
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
                clean_secret = str(secret_hash.get_secret(hashed_secret), "utf-8")
                print("#- Key: {} - Secret: {}".format(key, clean_secret))
                return clean_secret
            else:
                print("#- Key: {} not exist".format(key))
        else:
            print("!! Wrong password")
    else:
        print("#- User {} not exist".format(username))


def delete_user_from_db(username: str, password: str, db: Session):
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
            print("#- User {} deleted".format(username))
        else:
            print("!! Wrong password")
    else:
        print("#- User {} not exist".format(username))


def delete_secret_from_db(username: str, password: str, key: str, db: Session):
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
            print("#- Key {} deleted".format(key))
        else:
            print("!! Wrong password")
    else:
        print("#- User {} not exist".format(username))
