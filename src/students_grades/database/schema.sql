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
    FOREIGN KEY ( teacher_id) REFERENCES users ( teacher_id),
    FOREIGN KEY ( subject_id) REFERENCES users ( subject_id)
);