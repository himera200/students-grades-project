from src.students_grades.database.database import get_connection
from src.students_grades.models.teacher import Teacher


def _map(row) -> Teacher:
    return Teacher(*row)


_SELECT = """
    SELECT t.teacher_id, t.user_id, t.department,
           u.surname || ' ' || u.name
    FROM teachers t
    JOIN users u ON u.user_id = t.user_id
"""


def create(user_id: int, department: str) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO teachers (user_id, department)
        VALUES (?, ?)
    """, (user_id, department))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


def get_by_id(teacher_id: int) -> Teacher | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_SELECT + " WHERE t.teacher_id = ?", (teacher_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def get_by_user_id(user_id: int) -> Teacher | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_SELECT + " WHERE t.user_id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def get_all() -> list[Teacher]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_SELECT + " ORDER BY u.surname, u.name")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]


def update(teacher_id: int, department: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE teachers
        SET department = ?
        WHERE teacher_id = ?
    """, (department, teacher_id))
    conn.commit()
    conn.close()


def delete(teacher_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM teachers
        WHERE teacher_id = ?
    """, (teacher_id,))
    conn.commit()
    conn.close()
