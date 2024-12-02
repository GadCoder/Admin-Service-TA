
import abc

from src.app.domain.ports.repositories.teacher import TeacherRepositoryInterface

class TeacherUnitOfWorkInterface(abc.ABC):
    teachers: TeacherRepositoryInterface

    def __enter__(self) -> "TeacherUnitOfWorkInterface":
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
