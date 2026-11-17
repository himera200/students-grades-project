from src.students_grades.services import (
    admin_service,
    auth_service,
    grade_service,
)
from src.students_grades.ui_utils import (
    ask,
    ask_choice,
    ask_int,
    ask_optional,
    confirm,
    do,
    print_header,
    print_table,
    run,
)


def _avg(value) -> str:
    return "-" if value is None else f"{value:.2f}"


# ---------- Общие показы ----------

def _show_groups():
    print_table(
        ["ID", "Группа", "Курс", "Факультет"],
        [[g.group_id, g.name, g.course, g.faculty]
         for g in admin_service.get_groups()]
    )


def _show_subjects():
    print_table(
        ["ID", "Предмет", "Часы", "Семестр"],
        [[s.subject_id, s.name, s.hours, s.semester]
         for s in admin_service.get_subjects()]
    )


def _show_students():
    print_table(
        ["ID", "ФИО", "Группа", "Зачётка"],
        [[s.student_id, s.full_name, s.group_name, s.record_book_number]
         for s in admin_service.get_students()]
    )


def _show_teachers():
    print_table(
        ["ID", "ФИО", "Кафедра"],
        [[t.teacher_id, t.full_name, t.department]
         for t in admin_service.get_teachers()]
    )


def _show_grades(grades):
    print_table(
        ["ID", "Предмет", "Оценка", "Дата", "Преподаватель", "Комментарий"],
        [[g.grade_id, g.subject_name, g.value, g.grade_date,
          g.teacher_name, g.comment] for g in grades]
    )


# ---------- Студент ----------

def student_menu(user):
    student = run(auth_service.get_student_profile, user.user_id)
    if not student:
        return

    while True:
        print_header(f"Студент: {user.surname} {user.name}")
        print("1. Мои оценки")
        print("2. Средний балл")
        print("3. Задолженности")
        print("0. Выход")
        choice = ask_choice()

        if choice == "1":
            grades = run(grade_service.get_student_grades, student.student_id)
            if grades is not None:
                _show_grades(grades)
        elif choice == "2":
            grades = run(grade_service.get_student_grades, student.student_id)
            if grades is not None:
                avg = grade_service.calculate_average(grades)
                print(f"\nСредний балл: {_avg(avg)}")
        elif choice == "3":
            debts = run(grade_service.get_student_debts, student.student_id)
            if debts is not None:
                print_table(
                    ["Предмет", "Средний балл"],
                    [[name, _avg(avg)] for name, avg in debts]
                )
        elif choice == "0":
            break
        else:
            print("Неверный выбор")
