
from sqlmodel import  Field, SQLModel

class TeacherStudentLink(SQLModel, table=True):
    teacher_id: int| None  = Field(default=None,  foreign_key="teacher.teacher_code", primary_key=True)
    student_id: int | None = Field(default=None,  foreign_key="student.student_code", primary_key=True)
