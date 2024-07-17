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