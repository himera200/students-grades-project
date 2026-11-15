from src.students_grades.services import admin_service, auth_service
from src.students_grades.ui_utils import (
    ask, ask_choice, ask_int, ask_optional, do, print_header, print_table,
)


def login():
    print_header("Авторизация")
    login_value = ask("Логин")
    password_value = ask("Пароль")

    user = auth_service.authenticate(login_value, password_value)
    if not user:
        print("\nНеверный логин или пароль")
        return None

    print(f"\nДобро пожаловать, {user.name} {user.surname}")
    return user


def register():
    print_header("Регистрация")
    print("1. Студент")
    print("2. Преподаватель")
    print("0. Назад")
    role = ask_choice("Кто вы")

    if role not in ("1", "2"):
        return

    surname = ask("Фамилия")
    name = ask("Имя")
    patronymic = ask_optional("Отчество")
    email = ask("Email")
    login_value = ask("Логин")
    password_value = ask("Пароль (не короче 6 символов)")

    if role == "1":
        print_table(
            ["ID", "Группа", "Курс", "Факультет"],
            [[g.group_id, g.name, g.course, g.faculty]
             for g in admin_service.get_groups()]
        )
        group_id = ask_int("ID группы")
        record_book = ask("Номер зачётной книжки")
        do(auth_service.register_student, "Регистрация прошла успешно",
           surname, name, patronymic, email,
           login_value, password_value, group_id, record_book)
    else:
        department = ask("Кафедра")
        do(auth_service.register_teacher, "Регистрация прошла успешно",
           surname, name, patronymic, email,
           login_value, password_value, department)