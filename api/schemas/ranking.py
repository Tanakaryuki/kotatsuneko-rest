from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class RankingRequest(BaseModel):
    clear_time:  float = Field(..., example=1.23)
    
class RankingResponse(BaseModel):
    is_new: bool = Field(..., example=True)
    clear_time:  float = Field(..., example=1.23)
    update_at: datetime = Field(..., example="2021-01-01T00:00:00")
    
class RankingDate(BaseModel):
    username: str = Field(..., example="admin")
    clear_time:  float = Field(..., example=1.23)
    update_at: datetime = Field(..., example="2021-01-01T00:00:00")
    
class RankingListResponse(BaseModel):
    ranking_list: list[RankingDate] = Field(..., example=[{"clear_time":1.23,"update_at":"2021-01-01T00:00:00"}])
    
    
