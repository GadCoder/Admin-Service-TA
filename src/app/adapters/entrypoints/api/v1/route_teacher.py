import json

from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, Response, HTTPException, status
from dependency_injector.wiring import Provide, inject

from src.app.configurator.containers import Container
from src.app.domain.schemas.teacher import TeacherCreate
from src.app.domain.ports.use_cases.teacher import TeacherServiceInterface
from src.app.adapters.entrypoints.response_status_codes import STATUS_CODES

router = APIRouter()


@router.post("/create/")
@inject
async def create_user(
        teacher: TeacherCreate,
        teacher_service: TeacherServiceInterface = Depends(Provide[Container.teacher_service]),
):
    response = await teacher_service.create(teacher=teacher)
    data = jsonable_encoder(response.value)
    return Response(
        content=json.dumps(data),
        media_type="application/json",
        status_code=STATUS_CODES[response.type],
    )



@router.get("/get-by-code/")
@inject
def get_by_teacher_code(
        teacher_code: str,
        teacher_service: TeacherServiceInterface = Depends(Provide[Container.teacher_service]),
):
    response = teacher_service.get_by_code(teacher_code=teacher_code)
    data = jsonable_encoder(response.value)
    return Response(
        content=json.dumps(data),
        media_type="application/json",
        status_code=STATUS_CODES[response.type],
    )
