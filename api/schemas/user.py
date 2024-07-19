from pydantic import BaseModel, Field, EmailStr


class UserSignupRequest(BaseModel):
    username: str = Field(..., example="admin")
    omajinai: str = Field(..., example="password")

class UserExistsResponse(BaseModel):
    exists: bool

class Token(BaseModel):
    access_token: str
    token_type: str
