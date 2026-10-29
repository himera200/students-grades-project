DROP TABLE IF EXISTS grades;
DROP TABLE IF EXISTS teacher_subjects;
DROP TABLE IF EXISTS teachers;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS subjects;
DROP TABLE IF EXISTS student_groups;
DROP TABLE IF EXISTS user_roles;

CREATE TABLE user_roles (
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE student_groups (
    group_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    course INTEGER NOT NULL,
    faculty TEXT NOT NULL
);

CREATE TABLE subjects (
    subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    hours INTEGER NOT NULL,
    semester INTEGER NOT NULL
);

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    surname TEXT NOT NULL,
    name TEXT NOT NULL,
    patronymic TEXT,
    email TEXT NOT NULL UNIQUE,
    login TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role_id INTEGER NOT NULL,
    FOREIGN KEY (role_id) REFERENCES user_roles (role_id)
);
 
CREATE TABLE students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    group_id INTEGER NOT NULL,
    record_book_number TEXT NOT NULL UNIQUE,
    FOREIGN KEY ( user_id) REFERENCES users ( user_id),
    FOREIGN KEY ( group_id) REFERENCES student_groups ( group_id)
);

CREATE TABLE teachers (
    teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    department TEXT NOT NULL,
    FOREIGN KEY ( user_id) REFERENCES users ( user_id)
);

CREATE TABLE teacher_subjects (
    teacher_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    PRIMARY KEY ( teacher_id, subject_id),
    FOREIGN KEY ( teacher_id) REFERENCES teachers ( teacher_id),
    FOREIGN KEY ( subject_id) REFERENCES subjects ( subject_id)
);

CREATE TABLE grades (
    grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    teacher_id INTEGER NOT NULL,
    value INTEGER NOT NULL,
    grade_date TEXT NOT NULL,
    comment TEXT,
    FOREIGN KEY ( student_id) REFERENCES students ( student_id),
    FOREIGN KEY ( subject_id) REFERENCES subjects ( subject_id),
    FOREIGN KEY ( teacher_id) REFERENCES teachers ( teacher_id)
);

INSERT INTO user_roles (name)
VALUES ('Student'), ('Teacher'), ('Admin');

INSERT INTO student_groups (name, course, faculty)
VALUES ('ИВТ-21', 2, 'Информатика'), ('ИВТ-22', 2, 'Информатика'), ('ПИ-11', 1, 'Информатика');

INSERT INTO subjects ( name, hours, semester)
VALUES ('Информатика', 72, 1), ('Математика', 108, 1), ('Программирование', 144, 2), ('Базы данных', 108, 3);

INSERT INTO users (surname, name, patronymic, email, login, password_hash, role_id)
 VALUES ('Иванов', 'Иван', 'Иванович', 'ivanov@mail.ru', 'ivanov', 'hash1', 1), ('Петрова', 'Анна', 'Сергеевна', 'petrova@mail.ru', 'petrova', 'hash2', 1), ('Сидоров', 'Пётр', 'Алексеевич', 'sidorov@mail.ru', 'sidorov', 'hash3', 1), ('Смирнова', 'Ольга', 'Николаевна', 'smirnova@mail.ru', 'smirnova', 'hash4', 2), ('Козлов', 'Дмитрий', 'Андреевич', 'kozlov@mail.ru', 'kozlov', 'hash5', 2), ('Админов', 'Админ', NULL, 'admin@mail.ru', 'admin', 'hash6', 3);

 INSERT INTO students (user_id, group_id, record_book_number)
 VALUES (1, 1, 'ЗК-1001'), (2, 1, 'ЗК-1002'), (3, 2, 'ЗК-1003');

INSERT INTO teachers (user_id, department)
VALUES (4, 'Кафедра информатики'), (5, 'Кафедра математики');

INSERT INTO teacher_subjects (teacher_id, subject_id)
VALUES (1, 1), (1, 3), (1, 4), (2, 2);

INSERT INTO grades (student_id, subject_id, teacher_id, value, grade_date, comment)
VALUES (1, 1, 1, 5, '2026-10-01', 'Отлично'), (1, 3, 1, 4, '2026-10-10', NULL), (2, 1, 1, 4, '2026-10-01', NULL), (2, 2, 2, 3, '2026-10-05', 'Нужно подтянуть'), (3, 2, 2, 5, '2026-10-05', NULL), (3, 4, 1, 4, '2026-10-12', NULL);