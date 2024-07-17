from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class RankingRequest(BaseModel):
    clear_time:  float = Field(..., example=1.23)
    
class RankingResponse(BaseModel):
    is_new: bool = Field(..., example=True)
    clear_time:  float = Field(..., example=1.23)
    update_at: datetime = Field(..., example="2021-01-01T00:00:00")
