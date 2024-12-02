import json

from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, Response, HTTPException, status
from dependency_injector.wiring import Provide, inject

from src.app.configurator.containers import Container
from src.app.domain.schemas.assign_teacher_student import AssignTeacherStudent
from src.app.domain.ports.use_cases.student import StudentServiceInterface
from src.app.domain.ports.use_cases.teacher import TeacherServiceInterface
from src.app.adapters.entrypoints.response_status_codes import STATUS_CODES

router = APIRouter()


@router.patch("/assign-teacher-to-student")
@inject
def assign_teacher_to_student(
        assign_data: AssignTeacherStudent,
        student_service: StudentServiceInterface = Depends(Provide[Container.student_service]),
        teacher_service: TeacherServiceInterface = Depends(Provide[Container.teacher_service])
):
    teacher = teacher_service.get_by_code(assign_data.teacher_code).value
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found",
        )

    response = student_service.assign_teacher(assign_data=assign_data, teacher=teacher)
    data = jsonable_encoder(response.value)
    return Response(
        content=json.dumps(data),
        media_type="application/json",
        status_code=STATUS_CODES[response.type],
    )




