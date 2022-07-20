from sqlalchemy.orm import Session

from . import models, schemas

######################
#### create funcs ####
######################


def create_user(db: Session, user_info: schemas.UserInDBCreate):
    user_row = models.Users(
        username=user_info["username"],
        hashed_password=user_info["hashed_password"],
    )

    try:
        db.add(user_row)
        db.commit()
        db.refresh(user_row)
        # Close session
        db.expire_all()
        return True, "ok"
    except Exception as e:
        print(f"Eccezione: {e}")
        db.rollback()
        # Close session
        db.expire_all()
        return False, e.__class__.__name__


def create_key(db: Session, key_info: schemas.KeysCreate):
    key_row = models.Keys(
        user_id=key_info["user_id"],
        key_name=key_info["key_name"],
        hashed_secret=key_info["hashed_secret"],
    )

    try:
        db.add(key_row)
        db.commit()
        db.refresh(key_row)
        # Close session
        db.expire_all()
        return True, "ok"
    except Exception as e:
        print(f"Eccezione: {e}")
        db.rollback()
        # Close session
        db.expire_all()
        return False, e.__class__.__name__


######################
#### select funcs ####
######################


def get_all_user(db: Session):
    table = models.Users
    query_result = db.query(table).all()

    return [qr.username for qr in query_result]


def get_user(db: Session, username: str):
    table = models.Users
    query_result = db.query(table).filter(table.username == username).first()

    # Close session
    db.expire_all()

    return query_result


def get_secret(db: Session, key_name: str):
    table = models.Keys
    query_result = db.query(table).filter(table.key_name == key_name).first()

    # Close session
    db.expire_all()

    return query_result


def get_all_keys(db: Session, user_id: int):
    table = models.Keys
    query_result = db.query(table).filter(table.user_id == user_id).all()

    # Close session
    db.expire_all()

    return query_result


######################
#### select funcs ####
######################


def delete_user(db: Session, username: str):
    table = models.Users
    db.query(table).filter(table.username == username).delete(
        synchronize_session="evaluate"
    )
    db.commit()
    db.expire_all()


def delete_secret(db: Session, key: str):
    table = models.Keys
    db.query(table).filter(table.key_name == key).delete(synchronize_session="evaluate")
    db.commit()
    db.expire_all()
