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


            # ---------- Преподаватель ----------

def _pick_student_grade(teacher_id: int):
    """Выбор студента и показ его оценок. Возвращает student_id или None."""
    _show_students()
    student_id = ask_int("ID студента")
    grades = run(grade_service.get_student_grades, student_id)
    if grades is None:
        return None
    _show_grades(grades)
    return student_id if grades else None


def _add_grade(teacher):
    _show_students()
    student_id = ask_int("ID студента")

    subjects = admin_service.get_teacher_subjects(teacher.teacher_id)
    print_table(
        ["ID", "Предмет", "Часы", "Семестр"],
        [[s.subject_id, s.name, s.hours, s.semester] for s in subjects]
    )
    subject_id = ask_int("ID предмета")
    value = ask_int("Оценка (2-5)")
    comment = ask_optional("Комментарий")
    do(
        grade_service.add_grade,
        "Оценка выставлена",
        teacher.teacher_id, student_id, subject_id, value, comment
    )


def _edit_grade(teacher):
    if _pick_student_grade(teacher.teacher_id) is None:
        return
    grade_id = ask_int("ID оценки")
    value = ask_int("Новая оценка (2-5)")
    comment = ask_optional("Комментарий")
    do(
        grade_service.edit_grade,
        "Оценка изменена",
        teacher.teacher_id, grade_id, value, comment
    )


def _delete_grade(teacher):
    if _pick_student_grade(teacher.teacher_id) is None:
        return
    grade_id = ask_int("ID оценки")
    if confirm("Удалить оценку"):
        do(
            grade_service.delete_grade,
            "Оценка удалена",
            teacher.teacher_id, grade_id
        )


def _group_report():
    _show_groups()
    group_id = ask_int("ID группы")
    _show_subjects()
    subject_id = ask_int("ID предмета")
    report = run(grade_service.get_group_report, group_id, subject_id)
    if report is None:
        return
    print_table(
        ["Студент", "Оценки", "Средний балл", "Статус"],
        [[r["student"], ", ".join(map(str, r["grades"])) or "-",
          _avg(r["average"]), r["status"]] for r in report]
    )


def teacher_menu(user):
    teacher = run(auth_service.get_teacher_profile, user.user_id)
    if not teacher:
        return

    while True:
        print_header(f"Преподаватель: {user.surname} {user.name}")
        print("1. Мои предметы")
        print("2. Выставить оценку")
        print("3. Изменить оценку")
        print("4. Удалить оценку")
        print("5. Ведомость группы")
        print("0. Выход")
        choice = ask_choice()

        if choice == "1":
            subjects = admin_service.get_teacher_subjects(teacher.teacher_id)
            print_table(
                ["ID", "Предмет", "Часы", "Семестр"],
                [[s.subject_id, s.name, s.hours, s.semester]
                 for s in subjects]
            )
        elif choice == "2":
            _add_grade(teacher)
        elif choice == "3":
            _edit_grade(teacher)
        elif choice == "4":
            _delete_grade(teacher)
        elif choice == "5":
            _group_report()
        elif choice == "0":
            break
        else:
            print("Неверный выбор")
