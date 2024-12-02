from sqlmodel import SQLModel


class AssignTeacherStudent(SQLModel):
    auth_token: str
    student_code: str
    teacher_code: str