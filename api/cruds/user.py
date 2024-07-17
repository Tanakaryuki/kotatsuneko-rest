from passlib.context import CryptContext
from firebase_admin.firestore import client

import api.schemas.user as user_schema


def read_user_by_username(db: client, username: str) -> bool:
    user_ref = db.collection("Users").document(username).get()
    return user_ref.exists

def create_user(db: client, signup: user_schema.UserSignupRequest) -> None:
    signup_dict = signup.model_dump()
    signup_dict["hashed_omajinai"] = CryptContext(["bcrypt"]).hash(signup.hashed_omajinai)
    signup_dict.pop("username")
    user_ref = db.collection("Users").document(signup.username)
    user_ref.set(signup_dict)