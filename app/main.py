import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.logger import logger
from app.users.router import router as router_users
from app.materials.router import router as router_materials
from app.companies.router import router as router_companies
from app.deals.router import router as router_deals
from app.services.router import router as router_services
from app.stages.router import router as router_stages
from app.vehicles.router import router as router_vehicles


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
    allow_origins=["http://localhost:3000", "https://webhooktestjaremyapi.loca.lt"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "PUT", "DELETE", "OPTIONS"],
    # allow_headers=["*"],
    allow_headers=[
        "tg_news_bot_access_token",
        "TG_NEWS_BOT_ACCESS_TOKEN",
        "Authorization",
        "Content-Type"
    ],
    expose_headers=["*"]
)

app.include_router(router_users)
app.include_router(router_users)
app.include_router(router_materials)
app.include_router(router_companies)
app.include_router(router_deals)
app.include_router(router_services)
app.include_router(router_stages)
app.include_router(router_vehicles)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    # При подключении Prometheus + Grafana подобный лог не требуется
    logger.info("Request handling time", extra={
        "process_time": round(process_time, 4)
    })

    response.headers["Access-Control-Allow-Origin"] = request.headers.get("origin", "*")
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response


@app.get("/")
def read_root():
    return {
        "success": True,
        "message": "Welcome to telegram API"
    }
