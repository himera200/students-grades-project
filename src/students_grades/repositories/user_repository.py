from src.students_grades.database.database import get_connection
from src.students_grades.models.user import User


def _map(row) -> User:
    return User(*row)


def create(
    surname: str,
    name: str,
    patronymic: str | None,
    email: str,
    login: str,
    password_hash: str,
    role_id: int
) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (
            surname, name, patronymic,
            email, login, password_hash, role_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (surname, name, patronymic, email, login, password_hash, role_id))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


def get_by_id(user_id: int) -> User | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT u.user_id, u.surname, u.name, u.patronymic,
               u.email, u.login, u.password_hash, u.role_id,
               r.name
        FROM users u
        JOIN user_roles r ON r.role_id = u.role_id
        WHERE u.user_id = ?
    """, (user_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def get_by_login(login: str) -> User | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT u.user_id, u.surname, u.name, u.patronymic,
               u.email, u.login, u.password_hash, u.role_id,
               r.name
        FROM users u
        JOIN user_roles r ON r.role_id = u.role_id
        WHERE u.login = ?
    """, (login,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def get_by_email(email: str) -> User | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT u.user_id, u.surname, u.name, u.patronymic,
               u.email, u.login, u.password_hash, u.role_id,
               r.name
        FROM users u
        JOIN user_roles r ON r.role_id = u.role_id
        WHERE u.email = ?
    """, (email,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def get_all() -> list[User]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT u.user_id, u.surname, u.name, u.patronymic,
               u.email, u.login, u.password_hash, u.role_id,
               r.name
        FROM users u
        JOIN user_roles r ON r.role_id = u.role_id
        ORDER BY u.surname, u.name
    """)
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]


def update(
    user_id: int,
    surname: str,
    name: str,
    patronymic: str | None,
    email: str
):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE users
        SET surname = ?, name = ?, patronymic = ?, email = ?
        WHERE user_id = ?
    """, (surname, name, patronymic, email, user_id))
    conn.commit()
    conn.close()


def delete(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM users
        WHERE user_id = ?
    """, (user_id,))
    conn.commit()
    conn.close()
