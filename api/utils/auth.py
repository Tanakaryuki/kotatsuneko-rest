from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
import os
from fastapi.security import OAuth2PasswordBearer
from firebase_admin.firestore import client
from dotenv import load_dotenv

import api.cruds.user as user_crud


load_dotenv(verbose=True)
SECRET_KEY = str(os.getenv("SECRET_KEY"))
ALGORITHM = str(os.getenv("ALGORITHM"))
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")

def authenticate_user(db: client, username: str, password: str) -> bool:
    hashed_password = user_crud.read_user_hashed_omajinai(db=db, username=username)
    if hashed_password is None or not pwd_context.verify(password, hashed_password):
        return False
    return True

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

