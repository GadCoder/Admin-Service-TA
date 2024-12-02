import abc
from typing import Union

from src.app.domain.schemas import student as student_schema
from src.app.domain.models.teacher import Teacher
from src.app.domain.ports.unit_of_works.student import StudentUnitOfWorkInterface
from src.app.domain.ports.common.responses import ResponseFailure, ResponseSuccess
from src.app.domain.schemas.assign_teacher_student import AssignTeacherStudent
from src.app.domain.schemas.teacher import TeacherPublic


class StudentServiceInterface(abc.ABC):
    @abc.abstractmethod
    def __init__(self, uow: StudentUnitOfWorkInterface):
        self.uow = uow

    async def create(self, student: student_schema.StudentCreate) -> ResponseSuccess | ResponseFailure:
        return await self._create(student)

    def get_by_code(self, student_code: str) -> Union[ResponseSuccess, ResponseFailure]:
        return self._get_by_code(student_code)

    def assign_teacher(self, assign_data: AssignTeacherStudent, teacher: TeacherPublic) -> Union[ResponseSuccess, ResponseFailure]:
        return self._assign_teacher(assign_data, teacher)

    @abc.abstractmethod
    async def _create(
            self, user: student_schema.StudentCreate
    ) -> Union[ResponseSuccess, ResponseFailure]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_code(self, student_code: str) -> Union[ResponseSuccess, ResponseFailure]:
        raise NotImplementedError


    @abc.abstractmethod
    def _assign_teacher(self, assign_data: AssignTeacherStudent, teacher: TeacherPublic) -> Union[ResponseSuccess, ResponseFailure]:
        raise NotImplementedError
