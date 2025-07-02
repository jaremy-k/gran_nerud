import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.logger import logger
from app.users.router import router as router_users


@asynccontextmanager
async def lifespan(app: FastAPI):
    # при запуске
    yield


app = FastAPI(
    title="grand_nerud",
    version="0.1.0",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_users)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    # При подключении Prometheus + Grafana подобный лог не требуется
    logger.info("Request handling time", extra={
        "process_time": round(process_time, 4)
    })
    return response


@app.get("/")
def read_root():
    return {
        "success": True,
        "message": "Welcome to telegram API"
    }
