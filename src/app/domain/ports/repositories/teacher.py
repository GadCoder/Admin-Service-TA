import abc

from src.app.domain.schemas import teacher as teacher_schema

class TeacherRepositoryInterface(abc.ABC):
    def __init__(self):
        self.seen = set()

    def add(self, teacher: teacher_schema.TeacherCreate):
        self._add(teacher)
        self.seen.add(hash(teacher.teacher_code))

    def get_by_code(self, code: str) -> teacher_schema.TeacherPublic:
        teacher = self._get_by_code(code)
        if teacher:
            self.seen.add(hash(teacher.teacher_code))
        return teacher

    @abc.abstractmethod
    def _add(self, teacher: teacher_schema.TeacherCreate):
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_code(self, code: str) -> teacher_schema.TeacherPublic:
        raise NotImplementedError


