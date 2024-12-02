from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dependency_injector import containers, providers
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

from src.app.configurator import config
from src.app.adapters.use_cases.teacher import TeacherService
from src.app.adapters.use_cases.student import StudentService
from src.app.adapters.unit_of_works.student import StudentDatabaseUnitOfWork
from src.app.adapters.unit_of_works.teacher import TeacherDatabaseUnitOfWork

URL = config.get_database_uri()
print(f"URL: {URL}")
ENGINE = create_engine(url=URL)


def get_default_session_factory():
    return sessionmaker(bind=ENGINE)


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "src.app.adapters.entrypoints.api.v1",
        ]
    )

    SQLAlchemyInstrumentor().instrument(
        engine=ENGINE, enable_commenter=True, commenter_options={}
    )
    DEFAULT_SESSION_FACTORY = get_default_session_factory

    student_uow = providers.Singleton(
        StudentDatabaseUnitOfWork, session_factory=DEFAULT_SESSION_FACTORY
    )

    teacher_uow = providers.Singleton(
        TeacherDatabaseUnitOfWork, session_factory=DEFAULT_SESSION_FACTORY
    )

    student_service = providers.Factory(
        StudentService,
        uow=student_uow,
    )
    teacher_service = providers.Factory(
        TeacherService,
        uow=teacher_uow,
    )
