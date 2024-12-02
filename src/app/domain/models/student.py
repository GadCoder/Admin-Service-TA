from sqlmodel import Field, SQLModel, Relationship
from src.app.domain.models.teacher import Teacher, TeacherStudentLink

class Student(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    student_code: str = Field(max_length=8, unique=True)

    teachers: list[Teacher]  = Relationship(back_populates="students", link_model=TeacherStudentLink)
