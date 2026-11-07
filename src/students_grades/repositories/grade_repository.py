from src.students_grades.database.database import get_connection
from src.students_grades.models.grade import Grade


def _map(row) -> Grade:
    return Grade(*row)


_SELECT = """
    SELECT g.grade_id, g.student_id, g.subject_id, g.teacher_id,
           g.value, g.grade_date, g.comment,
           su.surname || ' ' || su.name,
           s.name,
           tu.surname || ' ' || tu.name
    FROM grades g
    JOIN students st ON st.student_id = g.student_id
    JOIN users su ON su.user_id = st.user_id
    JOIN subjects s ON s.subject_id = g.subject_id
    JOIN teachers t ON t.teacher_id = g.teacher_id
    JOIN users tu ON tu.user_id = t.user_id
"""


def create(
    student_id: int,
    subject_id: int,
    teacher_id: int,
    value: int,
    comment: str | None
) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO grades (
            student_id, subject_id, teacher_id,
            value, grade_date, comment
        )
        VALUES (?, ?, ?, ?, date('now'), ?)
    """, (student_id, subject_id, teacher_id, value, comment))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


def get_by_id(grade_id: int) -> Grade | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_SELECT + " WHERE g.grade_id = ?", (grade_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def get_by_student(student_id: int) -> list[Grade]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_SELECT + " WHERE g.student_id = ? ORDER BY g.grade_date DESC",
                (student_id,))
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]


def get_by_student_and_subject(student_id: int, subject_id: int) -> list[Grade]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_SELECT + """
        WHERE g.student_id = ? AND g.subject_id = ?
        ORDER BY g.grade_date DESC
    """, (student_id, subject_id))
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]


def get_by_group_and_subject(group_id: int, subject_id: int) -> list[Grade]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_SELECT + """
        WHERE st.group_id = ? AND g.subject_id = ?
        ORDER BY su.surname, g.grade_date
    """, (group_id, subject_id))
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]


def get_all() -> list[Grade]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_SELECT + " ORDER BY g.grade_date DESC")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]


def update(grade_id: int, value: int, comment: str | None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE grades
        SET value = ?, comment = ?
        WHERE grade_id = ?
    """, (value, comment, grade_id))
    conn.commit()
    conn.close()


def delete(grade_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM grades
        WHERE grade_id = ?
    """, (grade_id,))
    conn.commit()
    conn.close()