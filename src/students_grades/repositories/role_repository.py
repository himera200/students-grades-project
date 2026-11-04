from src.students_grades.database.database import get_connection
from src.students_grades.models.user_role import UserRole


def _map(row) -> UserRole:
    return UserRole(*row)


def get_by_id(role_id: int) -> UserRole | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT role_id, name
        FROM user_roles
        WHERE role_id = ?
    """, (role_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def get_by_name(name: str) -> UserRole | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT role_id, name
        FROM user_roles
        WHERE name = ?
    """, (name,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def get_all() -> list[UserRole]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT role_id, name
        FROM user_roles
        ORDER BY role_id
    """)
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]