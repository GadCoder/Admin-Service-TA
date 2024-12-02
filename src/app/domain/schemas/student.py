from sqlmodel import SQLModel

from src.app.domain.models.teacher import Teacher

class StudentCreate(SQLModel):
    auth_token: str
    student_code: str


class StudentPublic(SQLModel):
    id: int
    student_code: str
    teachers: list[Teacher]


class StudentUpdate(SQLModel):
    student_code: str
