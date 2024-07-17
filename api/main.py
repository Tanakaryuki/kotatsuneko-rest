from fastapi import FastAPI
from contextlib import asynccontextmanager
from firebase_admin import credentials,initialize_app
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)
SERVICE_ACCOUNT = str(os.getenv("SERVICE_ACCOUNT"))

from api.routers import user

@asynccontextmanager
async def lifespan(app: FastAPI):
    cred = credentials.Certificate(SERVICE_ACCOUNT)
    initialize_app(cred)
    print("Initializing Firebase")
    try:
        yield
    finally:
        print("Finalizing Firebase")
    
app = FastAPI(lifespan=lifespan)

@app.get("/")
async def hello():
    return {"message": "Hello World"}

app.include_router(user.router, prefix="/api", tags=["users"])