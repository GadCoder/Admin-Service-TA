from typing import Union

from src.app.adapters.entrypoints.api.utils import check_if_user_is_admin
from src.app.domain.ports.common.responses import (
    ResponseFailure,
    ResponseSuccess,
    ResponseTypes,
)

from src.app.domain.models.teacher import Teacher
from src.app.domain.schemas import teacher as teacher_schema
from src.app.domain.ports.use_cases.teacher import TeacherServiceInterface
from src.app.domain.ports.unit_of_works.teacher import TeacherUnitOfWorkInterface


def _handle_response_failure(
        teacher_code_: str = None, message: dict[str] = None
) -> ResponseFailure:
    if message:
        return ResponseFailure(ResponseTypes.RESOURCE_ERROR, message=message)
    return ResponseFailure(
        ResponseTypes.RESOURCE_ERROR,
        message={"detail": f"Teacher with code code {teacher_code_} not found"}
    )


class TeacherService(TeacherServiceInterface):
    def __init__(self, uow: TeacherUnitOfWorkInterface):
        self.uow = uow


    async def _create(self, teacher: teacher_schema.TeacherCreate ) -> Union[ResponseSuccess, ResponseFailure]:
        try:
            with self.uow:
                current_user_is_admin = check_if_user_is_admin(auth_token=teacher.auth_token)
                if current_user_is_admin is None:
                    return ResponseFailure(ResponseTypes.SYSTEM_ERROR, "System can't verify user")
                if not current_user_is_admin:
                    return ResponseFailure(ResponseTypes.SYSTEM_ERROR, "User is not authorized to perform this action")
                teacher_ = self.uow.teachers.get_by_code(teacher.teacher_code)
                if teacher_ is None:
                    new_teacher = Teacher(
                        teacher_code=teacher.teacher_code
                    )
                    self.uow.teachers.add(new_teacher)
                self.uow.commit()
                teacher_ = teacher_ or self.uow.teachers.get_by_code(teacher.teacher_code)
                teacher_output = teacher_schema.TeacherPublic(
                    id=teacher_.id,
                    teacher_code=teacher_.teacher_code,
                    students=teacher_.students
                )
                return ResponseSuccess(teacher_output)
        except Exception as e:
            return ResponseFailure(ResponseTypes.SYSTEM_ERROR, e)


    def _get_by_code(self, teacher_code: str) -> Union[ResponseSuccess, ResponseFailure]:
        try:
            teacher_ = self.uow.teachers.get_by_code(teacher_code)
            if teacher_:
                teacher_output = teacher_schema.TeacherPublic(
                    id=teacher_.id,
                    teacher_code=teacher_.teacher_code,
                    students=teacher_.students
                )
                return ResponseSuccess(teacher_output)
            return _handle_response_failure(teacher_code)
        except Exception as e:
            return ResponseFailure(ResponseTypes.SYSTEM_ERROR, e)


    def _get_as_obj(self, teacher_code: str) -> Union[ResponseSuccess, ResponseFailure]:
        try:
            teacher_ = self.uow.teachers.get_by_code(teacher_code)
            if teacher_:
                teacher_obj = self.uow.session.get(Teacher, teacher_.id)
                return ResponseSuccess(teacher_obj)
            return _handle_response_failure(teacher_code)
        except Exception as e:
            return ResponseFailure(ResponseTypes.SYSTEM_ERROR, e)