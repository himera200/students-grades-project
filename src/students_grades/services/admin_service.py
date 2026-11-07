from src.students_grades.models.student import Student
from src.students_grades.models.student_group import StudentGroup
from src.students_grades.models.subject import Subject
from src.students_grades.models.teacher import Teacher
from src.students_grades.repositories import (
    grade_repository,
    student_group_repository,
    student_repository,
    subject_repository,
    teacher_repository,
    teacher_subject_repository,
    user_repository,
)


# ---------- Справочник групп ----------

def get_groups() -> list[StudentGroup]:
    return student_group_repository.get_all()


def create_group(name: str, course: int, faculty: str):
    if not name.strip():
        raise ValueError("Название группы не может быть пустым")
    if not isinstance(course, int) or not 1 <= course <= 6:
        raise ValueError("Курс должен быть числом от 1 до 6")
    if not faculty.strip():
        raise ValueError("Факультет не может быть пустым")
    for g in student_group_repository.get_all():
        if g.name.lower() == name.strip().lower():
            raise ValueError("Группа с таким названием уже существует")
    student_group_repository.create(name.strip(), course, faculty.strip())


def delete_group(group_id: int):
    if not student_group_repository.get_by_id(group_id):
        raise ValueError("Группа не найдена")
    if student_repository.get_by_group(group_id):
        raise ValueError("Нельзя удалить группу, в которой есть студенты")
    student_group_repository.delete(group_id)


# ---------- Справочник предметов ----------

def get_subjects() -> list[Subject]:
    return subject_repository.get_all()


def create_subject(name: str, hours: int, semester: int):
    if not name.strip():
        raise ValueError("Название предмета не может быть пустым")
    if not isinstance(hours, int) or hours <= 0:
        raise ValueError("Количество часов должно быть положительным числом")
    if not isinstance(semester, int) or not 1 <= semester <= 12:
        raise ValueError("Семестр должен быть числом от 1 до 12")
    for s in subject_repository.get_all():
        if s.name.lower() == name.strip().lower():
            raise ValueError("Предмет с таким названием уже существует")
    subject_repository.create(name.strip(), hours, semester)


def delete_subject(subject_id: int):
    if not subject_repository.get_by_id(subject_id):
        raise ValueError("Предмет не найден")
    for g in grade_repository.get_all():
        if g.subject_id == subject_id:
            raise ValueError("Нельзя удалить предмет, по которому есть оценки")
    for t in teacher_subject_repository.get_teachers_by_subject(subject_id):
        teacher_subject_repository.unassign(t.teacher_id, subject_id)
    subject_repository.delete(subject_id)


# ---------- Назначение преподавателей ----------

def get_teachers() -> list[Teacher]:
    return teacher_repository.get_all()


def get_teacher_subjects(teacher_id: int) -> list[Subject]:
    return teacher_subject_repository.get_subjects_by_teacher(teacher_id)


def assign_teacher(teacher_id: int, subject_id: int):
    if not teacher_repository.get_by_id(teacher_id):
        raise ValueError("Преподаватель не найден")
    if not subject_repository.get_by_id(subject_id):
        raise ValueError("Предмет не найден")
    if teacher_subject_repository.is_assigned(teacher_id, subject_id):
        raise ValueError("Преподаватель уже назначен на этот предмет")
    teacher_subject_repository.assign(teacher_id, subject_id)


def unassign_teacher(teacher_id: int, subject_id: int):
    if not teacher_subject_repository.is_assigned(teacher_id, subject_id):
        raise ValueError("Такого назначения нет")
    teacher_subject_repository.unassign(teacher_id, subject_id)


# ---------- Учётные записи ----------

def get_students() -> list[Student]:
    return student_repository.get_all()


def delete_student(student_id: int):
    student = student_repository.get_by_id(student_id)
    if not student:
        raise ValueError("Студент не найден")
    if grade_repository.get_by_student(student_id):
        raise ValueError("Нельзя удалить студента, у которого есть оценки")
    student_repository.delete(student_id)
    user_repository.delete(student.user_id)


def delete_teacher(teacher_id: int):
    teacher = teacher_repository.get_by_id(teacher_id)
    if not teacher:
        raise ValueError("Преподаватель не найден")
    for g in grade_repository.get_all():
        if g.teacher_id == teacher_id:
            raise ValueError(
                "Нельзя удалить преподавателя, который выставлял оценки"
            )
    for s in teacher_subject_repository.get_subjects_by_teacher(teacher_id):
        teacher_subject_repository.unassign(teacher_id, s.subject_id)
    teacher_repository.delete(teacher_id)
    user_repository.delete(teacher.user_id)