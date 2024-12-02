from src.app.domain.models.teacher import Teacher
from src.app.domain.schemas import teacher as teacher_schema
from src.app.domain.ports.repositories.teacher import TeacherRepositoryInterface


class TeacherDatabaseRepository(TeacherRepositoryInterface):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, teacher):
        self.session.add(teacher)

    def _get_by_code(self, code: str) -> teacher_schema.TeacherPublic:
        return self.session.query(Teacher).filter(Teacher.teacher_code == code).first()

    def _get_as_obj(self, id):
        return self.session.get(Teacher, id)


