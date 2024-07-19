from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from firebase_admin.firestore import client

import api.schemas.user as user_schema
import api.cruds.user as user_crud
from api.db import get_db
from api.utils.auth import authenticate_user, create_access_token


router = APIRouter()

@router.post("/signup", description="新しいアカウントを作成するために使用されます。")
def signup(request: user_schema.UserSignupRequest, db:client = Depends(get_db)):
    user = user_crud.read_user_by_username(db=db, username=request.username)
    if user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    access_token = create_access_token(data={"sub": request.username})
    return user_schema.Token(access_token=access_token, token_type="bearer")

@router.get("/users/username/exists", description="指定されたユーザー名が存在するかどうかを確認します。",response_model=user_schema.UserExistsResponse)
def check_username(username: str, db:client = Depends(get_db)):
    user = user_crud.read_user_by_username(db=db, username=username)
    if user:
        return user_schema.UserExistsResponse(exists=True)
    else:
        return user_schema.UserExistsResponse(exists=False)
    
@router.post("/token", description="アクセストークンを取得するために使用されます。",response_model=user_schema.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db:client = Depends(get_db)):
    user = authenticate_user(db=db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = create_access_token(data={"sub": form_data.username})
    return user_schema.Token(access_token=access_token, token_type="bearer")
