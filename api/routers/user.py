from fastapi import APIRouter, Depends, HTTPException, status
from firebase_admin.firestore import client

import api.schemas.user as user_schema
import api.cruds.user as user_crud
from api.db import get_db


router = APIRouter()

@router.post("/signup", description="新しいアカウントを作成するために使用されます。")
def signup(request: user_schema.UserSignupRequest, db:client = Depends(get_db)):
    user = user_crud.read_user_by_username(db=db, username=request.username)
    if user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    user_crud.create_user(db=db, signup=request)
    return status.HTTP_201_CREATED

@router.get("/users/username/exists", description="指定されたユーザー名が存在するかどうかを確認します。")
def check_username(username: str, db:client = Depends(get_db)):
    user = user_crud.read_user_by_username(db=db, username=username)
    if user:
        return user_schema.UserExistsResponse(exists=True)
    else:
        return user_schema.UserExistsResponse(exists=False)
