from fastapi import FastAPI
from contextlib import asynccontextmanager
from firebase_admin import initialize_app
from fastapi.middleware.cors import CORSMiddleware

from api.routers import user,ranking

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_app()
    print("Initializing Firebase")
    try:
        yield
    finally:
        print("Finalizing Firebase")
    
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def hello():
    return {"message": "Hello World"}

app.include_router(user.router, prefix="/api", tags=["users"])
app.include_router(ranking.router, prefix="/api", tags=["ranking"])