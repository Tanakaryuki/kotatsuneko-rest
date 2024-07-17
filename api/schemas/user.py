from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class UserSignupRequest(BaseModel):
    username: str = Field(..., example="admin")
    hashed_omajinai: str = Field(..., example="password")

class UserExistsResponse(BaseModel):
    exists: bool
