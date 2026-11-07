import hashlib

from src.students_grades.models.user import User
from src.students_grades.repositories import (
    role_repository,
    student_group_repository,
    student_repository,
    teacher_repository,
    user_repository,
)

MIN_PASSWORD_LENGTH = 6


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def _validate_user_data(
    surname: str,
    name: str,
    email: str,
    login: str,
    password: str
):
    if not surname.strip():
        raise ValueError("Фамилия не может быть пустой")
    if not name.strip():
        raise ValueError("Имя не может быть пустым")
    if "@" not in email or "." not in email:
        raise ValueError("Некорректный email")
    if not login.strip():
        raise ValueError("Логин не может быть пустым")
    if len(password) < MIN_PASSWORD_LENGTH:
        raise ValueError(
            f"Пароль должен быть не короче {MIN_PASSWORD_LENGTH} символов"
        )
    if user_repository.get_by_login(login):
        raise ValueError("Логин уже занят")
    if user_repository.get_by_email(email):
        raise ValueError("Email уже зарегистрирован")


def _create_user(
    surname: str,
    name: str,
    patronymic: str | None,
    email: str,
    login: str,
    password: str,
    role_name: str
) -> int:
    role = role_repository.get_by_name(role_name)
    if not role:
        raise ValueError("Роль не найдена")
    return user_repository.create(
        surname.strip(),
        name.strip(),
        patronymic.strip() if patronymic and patronymic.strip() else None,
        email.strip(),
        login.strip(),
        hash_password(password),
        role.role_id
    )


def register_student(
    surname: str,
    name: str,
    patronymic: str | None,
    email: str,
    login: str,
    password: str,
    group_id: int,
    record_book_number: str
):
    _validate_user_data(surname, name, email, login, password)

    if not student_group_repository.get_by_id(group_id):
        raise ValueError("Группа не найдена")
    if not record_book_number.strip():
        raise ValueError("Номер зачётной книжки не может быть пустым")
    for s in student_repository.get_all():
        if s.record_book_number == record_book_number.strip():
            raise ValueError("Студент с таким номером зачётки уже есть")

    user_id = _create_user(
        surname, name, patronymic, email, login, password, "Student"
    )
    student_repository.create(user_id, group_id, record_book_number.strip())


def register_teacher(
    surname: str,
    name: str,
    patronymic: str | None,
    email: str,
    login: str,
    password: str,
    department: str
):
    _validate_user_data(surname, name, email, login, password)

    if not department.strip():
        raise ValueError("Кафедра не может быть пустой")

    user_id = _create_user(
        surname, name, patronymic, email, login, password, "Teacher"
    )
    teacher_repository.create(user_id, department.strip())


def authenticate(login: str, password: str) -> User | None:
    user = user_repository.get_by_login(login.strip())
    if not user:
        return None
    if user.password_hash != hash_password(password):
        return None
    return user