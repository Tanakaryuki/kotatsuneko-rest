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
    if ranking is None:
        clear_time,update_at = ranking_crud.create_ranking(db=db, ranking=request, username=current_user)
        ranking_list = ranking_crud.read_ranking(db=db,limit=request.limit)
        rank = -1
        for i, entry in enumerate(ranking_list):
            if entry['username'] == current_user:
                rank = i + 1
                break
        return ranking_schema.RankingResponse(rank=rank,clear_time=clear_time,update_at=update_at,is_new=True,ranking_list=ranking_list)
    if ranking.get("clear_time") > request.clear_time:
        clear_time,update_at = ranking_crud.create_ranking(db=db, ranking=request, username=current_user)
        ranking_list = ranking_crud.read_ranking(db=db,limit=request.limit)
        rank = -1
        for i, entry in enumerate(ranking_list):
            if entry['username'] == current_user:
                rank = i + 1
                break
        return ranking_schema.RankingResponse(rank=rank,clear_time=clear_time,update_at=update_at,is_new=True,ranking_list=ranking_list)
    ranking_list = ranking_crud.read_ranking(db=db,limit=request.limit)
    return ranking_schema.RankingResponse(rank=-1,clear_time=ranking.get("clear_time"),update_at=ranking.get("update_at"),is_new=False,ranking_list=ranking_list)

@router.get("/ranking", description="ランキングデータを取得するために使用されます。",response_model=ranking_schema.RankingListResponse)
def read_event(limit: int = 10, db: client = Depends(get_db)):
    ranking = ranking_crud.read_ranking(db=db,limit=limit)
    return ranking_schema.RankingListResponse(ranking_list=ranking)

@router.get("/record", description="自分の記録とランキングデータの比較のために使用されます。",response_model=ranking_schema.RankingRecordResponse)
def check_record(clear_time: int = 0,limit: int = 10, current_user: str = Depends(get_current_user), db: client = Depends(get_db)):
    ranking = ranking_crud.read_ranking_by_username(db=db,username=current_user)
    ranking_list = ranking_crud.read_ranking(db=db,limit=limit)
    if ranking is None:
        if len(ranking_list) >= limit:
            if ranking_list[limit - 1].get("clear_time") > clear_time:
                return ranking_schema.RankingRecordResponse(is_new=True,can_record=True,ranking_list=ranking_list,highest_clear_time=-1)
            else:
                return ranking_schema.RankingRecordResponse(is_new=True,can_record=False,ranking_list=ranking_list,highest_clear_time=-1)
        else:
            return ranking_schema.RankingRecordResponse(is_new=True,can_record=True,ranking_list=ranking_list,highest_clear_time=-1)
    if ranking.get("clear_time") > clear_time:
        if len(ranking_list) >= limit:
            if ranking_list[limit - 1].get("clear_time") > clear_time:
                return ranking_schema.RankingRecordResponse(is_new=True,can_record=True,ranking_list=ranking_list,highest_clear_time=ranking.get("clear_time"))
            else:
                return ranking_schema.RankingRecordResponse(is_new=True,can_record=False,ranking_list=ranking_list,highest_clear_time=ranking.get("clear_time"))
        else:
            return ranking_schema.RankingRecordResponse(is_new=True,can_record=True,ranking_list=ranking_list,highest_clear_time=ranking.get("clear_time"))
    return ranking_schema.RankingRecordResponse(is_new=False,can_record=False,ranking_list=ranking_list,highest_clear_time=ranking.get("clear_time"))