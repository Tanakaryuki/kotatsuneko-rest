from firebase_admin import firestore

def get_db():
    db = firestore.client()
    try:
        yield db
    finally:
        pass
