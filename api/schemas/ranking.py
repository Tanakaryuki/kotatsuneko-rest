from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class RankingRequest(BaseModel):
    clear_time:  int = Field(..., example=5)
    limit: int = Field(..., example=10)
    
class RankingResponse(BaseModel):
    rank: int = Field(..., example=1)
    is_new: bool = Field(..., example=True)
    clear_time:  int = Field(..., example=5)
    update_at: datetime = Field(..., example="2021-01-01T00:00:00")
    ranking_list: list[dict] = Field(..., example=[{"username":"admin","clear_time":5,"update_at":"2021-01-01T00:00:00"}])
    
class RankingDate(BaseModel):
    username: str = Field(..., example="admin")
    clear_time:  int = Field(..., example=5)
    update_at: datetime = Field(..., example="2021-01-01T00:00:00")
    
class RankingListResponse(BaseModel):
    ranking_list: list[RankingDate] = Field(..., example=[{"username":"admin","clear_time":5,"update_at":"2021-01-01T00:00:00"}])
    
class RankingRecordResponse(BaseModel):
    highest_clear_time: int = Field(..., example=5)
    is_new: bool = Field(..., example=True)
    can_record: bool = Field(..., example=True)
    ranking_list: list[RankingDate] = Field(..., example=[{"username":"admin","clear_time":5,"update_at":"2021-01-01T00:00:00"}]) 
