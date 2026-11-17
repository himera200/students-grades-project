from src.students_grades.auth import login, register
from src.students_grades.database.database import init_db
from src.students_grades.menu import admin_menu, student_menu, teacher_menu

STUDENT_ROLE_ID = 1
TEACHER_ROLE_ID = 2
ADMIN_ROLE_ID = 3


def main():
    init_db()

    while True:
        print("\n===== Система учёта оценок студентов =====")
        print("1. Вход")
        print("2. Регистрация")
        print("0. Выход")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            user = login()
            if not user:
                continue

            if user.role_id == STUDENT_ROLE_ID:
                student_menu(user)
            elif user.role_id == TEACHER_ROLE_ID:
                teacher_menu(user)
            elif user.role_id == ADMIN_ROLE_ID:
                admin_menu(user)
        elif choice == "2":
            register()
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неверный выбор")


if __name__ == "__main__":
    main()




