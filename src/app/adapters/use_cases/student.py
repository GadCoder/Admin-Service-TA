from typing import Union

from src.app.domain.ports.common.responses import (
    ResponseFailure,
    ResponseSuccess,
    ResponseTypes,
)

from src.app.domain.models.teacher import Teacher
from src.app.domain.models.student import Student
from src.app.domain.schemas import student as student_schema
from src.app.domain.ports.use_cases.student import StudentServiceInterface
from src.app.domain.ports.unit_of_works.student import StudentUnitOfWorkInterface
from src.app.adapters.entrypoints.api.utils import check_if_user_is_admin, get_teacher_by_code
from src.app.domain.schemas.assign_teacher_student import AssignTeacherStudent
from src.app.domain.schemas.teacher import TeacherPublic


def _handle_response_failure(
        student_code_: str = None, message: dict[str] = None
) -> ResponseFailure:
    if message:
        return ResponseFailure(ResponseTypes.RESOURCE_ERROR, message=message)
    return ResponseFailure(
        ResponseTypes.RESOURCE_ERROR,
        message={"detail": f"Student with code code {student_code_} not found"}
    )


class StudentService(StudentServiceInterface):
    def __init__(self, uow: StudentUnitOfWorkInterface):
        self.uow = uow


    async def _create(self, student: student_schema.StudentCreate ) -> Union[ResponseSuccess, ResponseFailure]:
        try:
            with self.uow:
                current_user_is_admin = check_if_user_is_admin(auth_token=student.auth_token)
                if current_user_is_admin is None:
                    return ResponseFailure(ResponseTypes.SYSTEM_ERROR, "System can't verify user")
                if not current_user_is_admin:
                    return ResponseFailure(ResponseTypes.SYSTEM_ERROR, "User is not authorized to perform this action")
                student_ = self.uow.students.get_by_code(student.student_code)
                if student_ is None:
                    new_student = Student(
                        student_code=student.student_code
                    )
                    self.uow.students.add(new_student)
                self.uow.commit()
                student_ = student_ or self.uow.students.get_by_code(student.student_code)
                student_output = student_schema.StudentPublic(
                    id=student_.id,
                    student_code=student_.student_code,
                    teachers=student_.teachers,
                )
                return ResponseSuccess(student_output)
        except Exception as e:
            return ResponseFailure(ResponseTypes.SYSTEM_ERROR, e)


    def _get_by_code(self, student_code: str) -> Union[ResponseSuccess, ResponseFailure]:
        try:
            student_ = self.uow.students.get_by_code(student_code)
            if student_:
                student_output = student_schema.StudentPublic(
                    id=student_.id,
                    student_code=student_.student_code,
                    teachers=student_.teachers,
                )
                return ResponseSuccess(student_output)
            return _handle_response_failure(student_code)
        except Exception as e:
            return ResponseFailure(ResponseTypes.SYSTEM_ERROR, e)


    def _assign_teacher(self, assign_data: AssignTeacherStudent, teacher: TeacherPublic) -> Union[ResponseSuccess, ResponseFailure]:
        try:
            current_user_is_admin = check_if_user_is_admin(auth_token=assign_data.auth_token)
            if current_user_is_admin is None:
                return ResponseFailure(ResponseTypes.SYSTEM_ERROR, "System can't verify user")
            if not current_user_is_admin:
                return ResponseFailure(ResponseTypes.SYSTEM_ERROR, "User is not authorized to perform this action")
            student_ = self.uow.students.get_by_code(assign_data.student_code)
            if student_ and teacher:
                teacher_obj = self.uow.session.get(Teacher, teacher.id)
                student_.teachers = student_.teachers + [teacher_obj]
                self.uow.commit()
                student_output = student_schema.StudentPublic(
                    id=student_.id,
                    student_code=student_.student_code,
                    teachers=student_.teachers,
                )
                return ResponseSuccess(student_output)
            return _handle_response_failure(assign_data.teacher_code)
        except Exception as e:
            return ResponseFailure(ResponseTypes.SYSTEM_ERROR, e)