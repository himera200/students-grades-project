from src.students_grades.database.database import get_connection
from src.students_grades.models.student import Student


def _map(row) -> Student:
    return Student(*row)


_SELECT = """
    SELECT s.student_id, s.user_id, s.group_id, s.record_book_number,
           u.surname || ' ' || u.name,
           g.name
    FROM students s
    JOIN users u ON u.user_id = s.user_id
    JOIN student_groups g ON g.group_id = s.group_id
"""


def create(user_id: int, group_id: int, record_book_number: str) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO students (user_id, group_id, record_book_number)
        VALUES (?, ?, ?)
    """, (user_id, group_id, record_book_number))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


def get_by_id(student_id: int) -> Student | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_SELECT + " WHERE s.student_id = ?", (student_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def get_by_user_id(user_id: int) -> Student | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_SELECT + " WHERE s.user_id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def get_all() -> list[Student]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_SELECT + " ORDER BY u.surname, u.name")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]


def get_by_group(group_id: int) -> list[Student]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_SELECT + " WHERE s.group_id = ? ORDER BY u.surname, u.name",
                (group_id,))
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]


def update(student_id: int, group_id: int, record_book_number: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE students
        SET group_id = ?, record_book_number = ?
        WHERE student_id = ?
    """, (group_id, record_book_number, student_id))
    conn.commit()
    conn.close()


def delete(student_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM students
        WHERE student_id = ?
    """, (student_id,))
    conn.commit()
    conn.close()