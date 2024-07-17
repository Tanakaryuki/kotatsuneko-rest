from datetime import datetime
from firebase_admin.firestore import client

import api.schemas.ranking as ranking_schema


def create_ranking(db: client, ranking: ranking_schema.RankingRequest, username: str) -> tuple:
    ranking_dict = ranking.model_dump()
    ranking_dict["update_at"] = datetime.now()
    user_ref = db.collection("Ranking").document(username)
    user_ref.set(ranking_dict)
    return ranking_dict.get("clear_time"), ranking_dict.get("update_at")
    
def read_ranking_by_username(db: client, username: str) -> dict|None:
    ranking_ref = db.collection("Ranking").document(username).get()
    if ranking_ref.exists:
        return ranking_ref
    return None

def read_ranking(db: client, limit: int = 10) -> list:
    ranking_list = []
    ranking_ref = db.collection("Ranking").order_by("clear_time").limit(limit).stream()
    for doc in ranking_ref:
        ranking_dict = doc.to_dict()
        ranking_dict["username"] = doc.id
        ranking_list.append(ranking_dict)
    return ranking_list