import time
from fastapi import FastAPI, Request
from app.utils.request_logging import logging_request_time
from app.routes.user_auth import router as auth_router
from app.routes.user import router as user_router
from app.routes.model_inference import router as model_router
from datetime import datetime

app = FastAPI()

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