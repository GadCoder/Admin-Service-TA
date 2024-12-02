from typing import Any, Callable

from sqlalchemy.orm import Session

from src.app.adapters.repositories.student import StudentDatabaseRepository
from src.app.domain.ports.unit_of_works.student import StudentUnitOfWorkInterface


class StudentDatabaseUnitOfWork(StudentUnitOfWorkInterface):
    def __init__(self, session_factory: Callable[[], Any]):
        self.session_factory = session_factory()

    def __enter__(self):
        self.session: Session = self.session_factory()
        self.students = StudentDatabaseRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def _commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
