from src.students_grades.models.grade import Grade
from src.students_grades.repositories import (
    grade_repository,
    student_group_repository,
    student_repository,
    subject_repository,
    teacher_repository,
    teacher_subject_repository,
)

MIN_GRADE = 2
MAX_GRADE = 5
DEBT_THRESHOLD = 3.0


def _check_value(value: int):
    if not isinstance(value, int) or not MIN_GRADE <= value <= MAX_GRADE:
        raise ValueError(
            f"Оценка должна быть целым числом от {MIN_GRADE} до {MAX_GRADE}"
        )


def add_grade(
    teacher_id: int,
    student_id: int,
    subject_id: int,
    value: int,
    comment: str | None
):
    _check_value(value)

    if not teacher_repository.get_by_id(teacher_id):
        raise ValueError("Преподаватель не найден")
    if not student_repository.get_by_id(student_id):
        raise ValueError("Студент не найден")
    if not subject_repository.get_by_id(subject_id):
        raise ValueError("Предмет не найден")
    if not teacher_subject_repository.is_assigned(teacher_id, subject_id):
        raise ValueError("Преподаватель не ведёт этот предмет")

    comment = comment.strip() if comment and comment.strip() else None
    grade_repository.create(
        student_id, subject_id, teacher_id, value, comment
    )


def edit_grade(
    teacher_id: int,
    grade_id: int,
    value: int,
    comment: str | None
):
    _check_value(value)

    grade = grade_repository.get_by_id(grade_id)
    if not grade:
        raise ValueError("Оценка не найдена")
    if grade.teacher_id != teacher_id:
        raise ValueError("Можно изменять только свои оценки")

    comment = comment.strip() if comment and comment.strip() else None
    grade_repository.update(grade_id, value, comment)


def delete_grade(teacher_id: int, grade_id: int):
    grade = grade_repository.get_by_id(grade_id)
    if not grade:
        raise ValueError("Оценка не найдена")
    if grade.teacher_id != teacher_id:
        raise ValueError("Можно удалять только свои оценки")
    grade_repository.delete(grade_id)


def get_student_grades(student_id: int) -> list[Grade]:
    if not student_repository.get_by_id(student_id):
        raise ValueError("Студент не найден")
    return grade_repository.get_by_student(student_id)


def calculate_average(grades: list[Grade]) -> float | None:
    if not grades:
        return None
    return sum(g.value for g in grades) / len(grades)


def get_student_average(student_id: int) -> float | None:
    return calculate_average(get_student_grades(student_id))


def get_student_debts(student_id: int) -> list[tuple[str, float]]:
    grades = get_student_grades(student_id)
    by_subject: dict[str, list[Grade]] = {}
    for g in grades:
        by_subject.setdefault(g.subject_name, []).append(g)

    debts = []
    for subject_name, subject_grades in by_subject.items():
        avg = calculate_average(subject_grades)
        if avg < DEBT_THRESHOLD:
            debts.append((subject_name, avg))
    return debts


def get_group_report(group_id: int, subject_id: int) -> list[dict]:
    if not student_group_repository.get_by_id(group_id):
        raise ValueError("Группа не найдена")
    if not subject_repository.get_by_id(subject_id):
        raise ValueError("Предмет не найден")

    report = []
    for student in student_repository.get_by_group(group_id):
        grades = grade_repository.get_by_student_and_subject(
            student.student_id, subject_id
        )
        avg = calculate_average(grades)
        if avg is None:
            status = "нет оценок"
        elif avg < DEBT_THRESHOLD:
            status = "на риске отчисления"
        else:
            status = "успевает"
        report.append({
            "student": student.full_name,
            "grades": [g.value for g in grades],
            "average": avg,
            "status": status,
        })
    return report