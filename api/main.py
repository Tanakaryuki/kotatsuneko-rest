import logging
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from firebase_admin import initialize_app
from fastapi.middleware.cors import CORSMiddleware

from api.routers import user, ranking

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_app()
    print("Initializing Firebase")
    try:
        yield
    finally:
        print("Finalizing Firebase")
    
app = FastAPI(lifespan=lifespan)

app = FastAPI(lifespan=lifespan)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    body = await request.body()
    logger.info(f"Request: {request.method} {request.url} {body.decode('utf-8').replace('\n', '')}")
    
    response = await call_next(request)
    
    return response

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
