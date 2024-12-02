from sqlmodel import  SQLModel

from src.app.domain.models.student import Student

class TeacherCreate(SQLModel):
    auth_token: str
    teacher_code: str

class TeacherPublic(SQLModel):
    id: int
    teacher_code: str
    students: list[Student]


class TeacherAssign(SQLModel):
    teacher_code: str


