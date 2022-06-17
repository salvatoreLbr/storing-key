from pydantic import BaseModel


class KeysBase(BaseModel):
    user_id: int
    key_name: str
    hashed_secret: str


class KeysCreate(KeysBase):
    pass


class Keys(KeysBase):
    id: int
    user_id: int
    key_name: str
    hashed_secret: str


class User(BaseModel):
    username: str


class UserInDB(User):
    hashed_password: str


class UserInDBCreate(UserInDB):
    pass
