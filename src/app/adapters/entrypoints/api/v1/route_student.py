import json

from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, Response, HTTPException, status
from dependency_injector.wiring import Provide, inject

from src.app.configurator.containers import Container
from src.app.domain.schemas.student import StudentCreate
from src.app.domain.ports.use_cases.student import StudentServiceInterface
from src.app.adapters.entrypoints.response_status_codes import STATUS_CODES

router = APIRouter()


@router.post("/create/")
@inject
async def create_student(
        student: StudentCreate,
        student_service: StudentServiceInterface = Depends(Provide[Container.student_service]),
):
    response = await student_service.create(student=student)
    data = jsonable_encoder(response.value)
    return Response(
        content=json.dumps(data),
        media_type="application/json",
        status_code=STATUS_CODES[response.type],)


@router.get("/get-by-code/")
@inject
def get_by_student_code(
        student_code: str,
        student_service: StudentServiceInterface = Depends(Provide[Container.student_service]),
):
    response = student_service.get_by_code(student_code=student_code)
    data = jsonable_encoder(response.value)
    return Response(
        content=json.dumps(data),
        media_type="application/json",
        status_code=STATUS_CODES[response.type],
    )


