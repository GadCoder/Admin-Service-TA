import abc

from src.app.domain.ports.repositories.student import StudentRepositoryInterface

class StudentUnitOfWorkInterface(abc.ABC):
    students: StudentRepositoryInterface

    def __enter__(self) -> "StudentUnitOfWorkInterface":
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self._commit()

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError
