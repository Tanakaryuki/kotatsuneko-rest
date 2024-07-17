from fastapi import APIRouter, Depends, Response, status
from firebase_admin.firestore import client

import api.schemas.ranking as ranking_schema
import api.cruds.ranking as ranking_crud
from api.utils.auth import get_current_user
from api.db import get_db

router = APIRouter()

@router.post("/ranking", description="ランキングデータを更新するために使用されます。",response_model=ranking_schema.RankingResponse)
def create_event(request: ranking_schema.RankingRequest,current_user: str = Depends(get_current_user), db: client = Depends(get_db)):
    ranking = ranking_crud.read_ranking_by_username(db=db,username=current_user)
    print(ranking)
    if ranking is None:
        clear_time,update_at = ranking_crud.create_ranking(db=db, ranking=request, username=current_user)
        return ranking_schema.RankingResponse(clear_time=clear_time,update_at=update_at,is_new=True)
    if ranking.get("clear_time") > request.clear_time:
        clear_time,update_at = ranking_crud.create_ranking(db=db, ranking=request, username=current_user)
        return ranking_schema.RankingResponse(clear_time=clear_time,update_at=update_at,is_new=True)
    return ranking_schema.RankingResponse(clear_time=ranking.get("clear_time"),update_at=ranking.get("update_at"),is_new=False)