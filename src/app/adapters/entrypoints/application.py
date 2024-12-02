from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.app.adapters.entrypoints.api.base import api_router
from src.app.adapters.db.orm import create_db_and_tables
from src.app.configurator.config import settings
from src.app.configurator.containers import Container


def include_router(app_):
    app_.include_router(api_router)


def add_cors(app_):
    origins = ["*"]
    app_.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def start_application():
    container = Container()
    app_ = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    app_.container = container
    include_router(app_)
    create_db_and_tables()
    add_cors(app_)
    return app_


app = start_application()
