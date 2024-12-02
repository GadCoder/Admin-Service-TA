from fastapi import FastAPI

from src.app.adapters.entrypoints.api.base import api_router
from src.app.adapters.db.orm import create_db_and_tables
from src.app.configurator.config import settings
from src.app.configurator.containers import Container


def include_router(app_):
    app_.include_router(api_router)


def start_application():
    container = Container()
    app_ = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    app_.container = container
    include_router(app_)
    create_db_and_tables()
    return app_


app = start_application()
