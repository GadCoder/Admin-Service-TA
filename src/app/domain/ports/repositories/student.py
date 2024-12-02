import abc

from src.app.domain.schemas import student as student_schema

class StudentRepositoryInterface(abc.ABC):
    def __init__(self):
        self.seen = set()

    def add(self, student: student_schema.StudentCreate):
        self._add(student)
        self.seen.add(hash(student.student_code))

    def get_by_code(self, code: str) -> student_schema.StudentPublic:
        student = self._get_by_code(code)
        if student:
            self.seen.add(hash(student.student_code))
        return student

    @abc.abstractmethod
    def _add(self, student: student_schema.StudentCreate):
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_code(self, code: str) -> student_schema.StudentPublic:
        raise NotImplementedError


