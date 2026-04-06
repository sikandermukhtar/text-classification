import time
from fastapi import FastAPI, Request
from app.utils.request_logging import logging_request_time
from app.routes.user_auth import router as auth_router
from app.routes.user import router as user_router
from app.routes.model_inference import router as model_router
from datetime import datetime

import joblib
from pathlib import Path
from contextlib import asynccontextmanager
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent.parent 
QUORA_MODEL_PATH = BASE_DIR / "model" / "trained_models" / "quora_classifier.pkl"
IMDB_MODEL_PATH = BASE_DIR / "model" / "trained_models" / "imdb_classifier.pkl"

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load models at startup
    app.state.embedder = SentenceTransformer("all-MiniLM-L6-v2")
    app.state.quora_classifier = joblib.load(QUORA_MODEL_PATH)
    app.state.imdb_classifier = joblib.load(IMDB_MODEL_PATH)
    yield
    # Clean up models (if necessary)
    del app.state.embedder
    del app.state.quora_classifier
    del app.state.imdb_classifier

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(model_router)

@app.get("/")
def index():
    return {"message": "Hello World"}

@app.middleware("http")
async def request_time_tracking(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    response_time = time.perf_counter() - start_time
    request_url = str(request.url)
    current_time = datetime.now().strftime("%A %B %d, %Y at %I:%M:%S %p")
    status = response.status_code
    logging_request_time(request_url, response_time, current_time, status)
    return response