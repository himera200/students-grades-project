from src.students_grades.database.database import get_connection
from src.students_grades.models.subject import Subject
from src.students_grades.models.teacher import Teacher


def assign(teacher_id: int, subject_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO teacher_subjects (teacher_id, subject_id)
        VALUES (?, ?)
    """, (teacher_id, subject_id))
    conn.commit()
    conn.close()


def unassign(teacher_id: int, subject_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM teacher_subjects
        WHERE teacher_id = ? AND subject_id = ?
    """, (teacher_id, subject_id))
    conn.commit()
    conn.close()


def is_assigned(teacher_id: int, subject_id: int) -> bool:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 1
        FROM teacher_subjects
        WHERE teacher_id = ? AND subject_id = ?
    """, (teacher_id, subject_id))
    row = cur.fetchone()
    conn.close()
    return row is not None


def get_subjects_by_teacher(teacher_id: int) -> list[Subject]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT s.subject_id, s.name, s.hours, s.semester
        FROM teacher_subjects ts
        JOIN subjects s ON s.subject_id = ts.subject_id
        WHERE ts.teacher_id = ?
        ORDER BY s.name
    """, (teacher_id,))
    rows = cur.fetchall()
    conn.close()
    return [Subject(*r) for r in rows]


def get_teachers_by_subject(subject_id: int) -> list[Teacher]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT t.teacher_id, t.user_id, t.department,
               u.surname || ' ' || u.name
        FROM teacher_subjects ts
        JOIN teachers t ON t.teacher_id = ts.teacher_id
        JOIN users u ON u.user_id = t.user_id
        WHERE ts.subject_id = ?
        ORDER BY u.surname, u.name
    """, (subject_id,))
    rows = cur.fetchall()
    conn.close()
    return [Teacher(*r) for r in rows]
