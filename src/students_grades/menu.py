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


            # ---------- Администратор ----------

def _groups_menu():
    while True:
        print_header("Группы")
        print("1. Показать")
        print("2. Добавить")
        print("3. Удалить")
        print("0. Назад")
        choice = ask_choice()

        if choice == "1":
            _show_groups()
        elif choice == "2":
            name = ask("Название")
            course = ask_int("Курс", 1, 6)
            faculty = ask("Факультет")
            do(admin_service.create_group, "Группа добавлена",
               name, course, faculty)
        elif choice == "3":
            _show_groups()
            group_id = ask_int("ID группы")
            do(admin_service.delete_group, "Группа удалена", group_id)
        elif choice == "0":
            break
        else:
            print("Неверный выбор")


def _subjects_menu():
    while True:
        print_header("Предметы")
        print("1. Показать")
        print("2. Добавить")
        print("3. Удалить")
        print("0. Назад")
        choice = ask_choice()

        if choice == "1":
            _show_subjects()
        elif choice == "2":
            name = ask("Название")
            hours = ask_int("Количество часов", 1)
            semester = ask_int("Семестр", 1, 12)
            do(admin_service.create_subject, "Предмет добавлен",
               name, hours, semester)
        elif choice == "3":
            _show_subjects()
            subject_id = ask_int("ID предмета")
            do(admin_service.delete_subject, "Предмет удалён", subject_id)
        elif choice == "0":
            break
        else:
            print("Неверный выбор")


def _students_menu():
    while True:
        print_header("Студенты")
        print("1. Показать")
        print("2. Удалить")
        print("0. Назад")
        choice = ask_choice()

        if choice == "1":
            _show_students()
        elif choice == "2":
            _show_students()
            student_id = ask_int("ID студента")
            if confirm("Удалить студента"):
                do(admin_service.delete_student, "Студент удалён", student_id)
        elif choice == "0":
            break
        else:
            print("Неверный выбор")


def _teachers_menu():
    while True:
        print_header("Преподаватели")
        print("1. Показать")
        print("2. Назначить на предмет")
        print("3. Снять с предмета")
        print("4. Удалить")
        print("0. Назад")
        choice = ask_choice()

        if choice == "1":
            _show_teachers()
        elif choice == "2":
            _show_teachers()
            teacher_id = ask_int("ID преподавателя")
            _show_subjects()
            subject_id = ask_int("ID предмета")
            do(admin_service.assign_teacher, "Преподаватель назначен",
               teacher_id, subject_id)
        elif choice == "3":
            _show_teachers()
            teacher_id = ask_int("ID преподавателя")
            subjects = run(admin_service.get_teacher_subjects, teacher_id)
            if subjects is not None:
                print_table(
                    ["ID", "Предмет"],
                    [[s.subject_id, s.name] for s in subjects]
                )
            subject_id = ask_int("ID предмета")
            do(admin_service.unassign_teacher, "Назначение снято",
               teacher_id, subject_id)
        elif choice == "4":
            _show_teachers()
            teacher_id = ask_int("ID преподавателя")
            if confirm("Удалить преподавателя"):
                do(admin_service.delete_teacher, "Преподаватель удалён",
                   teacher_id)
        elif choice == "0":
            break
        else:
            print("Неверный выбор")


def admin_menu(user):
    while True:
        print_header(f"Администратор: {user.login}")
        print("1. Группы")
        print("2. Предметы")
        print("3. Студенты")
        print("4. Преподаватели")
        print("0. Выход")
        choice = ask_choice()

        if choice == "1":
            _groups_menu()
        elif choice == "2":
            _subjects_menu()
        elif choice == "3":
            _students_menu()
        elif choice == "4":
            _teachers_menu()
        elif choice == "0":
            break
        else:
            print("Неверный выбор")


