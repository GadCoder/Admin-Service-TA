from sqlmodel import SQLModel
from src.app.configurator.containers import ENGINE


def create_db_and_tables():
    SQLModel.metadata.create_all(ENGINE)
