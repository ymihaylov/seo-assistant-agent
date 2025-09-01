import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import inspect

import app.models
from app.api.endpoints import api_router
from app.api.endpoints import jobs as jobs_endpoints
from app.api.endpoints import sessions as sessions_endpoints
from app.api.middlewares import register_middlewares
from app.core.database import engine, Base, DATABASE_URL
from app.core.settings import get_settings


def _ensure_sqlite_dir():
    if DATABASE_URL.startswith("sqlite:///"):
        path = DATABASE_URL.replace("sqlite:///", "", 1)
        d = os.path.dirname(path)
        if d and not os.path.exists(d):
            os.makedirs(d, exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    _ensure_sqlite_dir()
    Base.metadata.create_all(bind=engine)
    insp = inspect(engine)
    print("Tables detected:", insp.get_table_names())
    yield


def create_app() -> FastAPI:
    s = get_settings()

    app = FastAPI(
        title="SEO Assistant API",
        description="A FastAPI application for AI-powered SEO Assistant",
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    register_middlewares(app)

    app.include_router(api_router)
    app.include_router(sessions_endpoints.router)
    app.include_router(jobs_endpoints.router)

    return app


app = create_app()
