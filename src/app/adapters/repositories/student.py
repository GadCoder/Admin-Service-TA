from src.app.domain.models.student import Student
from src.app.domain.schemas import student as student_schema
from src.app.domain.ports.repositories.student import StudentRepositoryInterface


class StudentDatabaseRepository(StudentRepositoryInterface):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, student):
        self.session.add(student)

    def _get_by_code(self, code: str) -> student_schema.StudentPublic:
        return self.session.query(Student).filter(Student.student_code == code).first()


