import abc
from typing import Union

from src.app.domain.schemas import teacher as teacher_schema
from src.app.domain.ports.unit_of_works.teacher import TeacherUnitOfWorkInterface
from src.app.domain.ports.common.responses import ResponseFailure, ResponseSuccess

class TeacherServiceInterface(abc.ABC):
    @abc.abstractmethod
    def __init__(self, uow: TeacherUnitOfWorkInterface):
        self.uow = uow

    async def create(self, teacher: teacher_schema.TeacherCreate) -> ResponseSuccess | ResponseFailure:
        return await self._create(teacher)

    def get_by_code(self, teacher_code: str) -> Union[ResponseSuccess, ResponseFailure]:
        return self._get_by_code(teacher_code)

    def get_as_obj(self, teacher_code: str):
        return self._get_as_obj(teacher_code)

    @abc.abstractmethod
    async def _create(
            self, user: teacher_schema.TeacherCreate
    ) -> Union[ResponseSuccess, ResponseFailure]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_code(self, teacher_code: str) -> Union[ResponseSuccess, ResponseFailure]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_as_obj(self, teacher_code: str):
        raise NotImplementedError
