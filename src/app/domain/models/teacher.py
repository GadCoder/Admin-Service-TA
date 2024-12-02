from sqlmodel import Field, SQLModel, Relationship

from src.app.domain.models.student_teacher import TeacherStudentLink


class Teacher(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    teacher_code: str = Field(unique=True)
    students: list["Student"] = Relationship(back_populates="teachers", link_model=TeacherStudentLink)
