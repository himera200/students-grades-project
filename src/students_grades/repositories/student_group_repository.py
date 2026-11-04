from src.students_grades.database.database import get_connection 
from src.students_grades.models.student_group import StudentGroup

def _map(row) -> StudentGroup: 
    return StudentGroup(*row)

def create(name: str, course: int, faculty: str): 
    conn = get_connection() 
    cur = conn.cursor() 
    cur.execute(""" INSERT INTO student_groups (name, course, faculty) VALUES (?, ?, ?) """, (name, course, faculty)) 
    conn.commit() 
    conn.close()

def get_by_id(group_id: int) -> StudentGroup | None: 
    conn = get_connection() 
    cur = conn.cursor() 
    cur.execute(""" SELECT group_id, name, course, faculty FROM student_groups WHERE group_id = ? """, (group_id,)) 
    row = cur.fetchone() 
    conn.close() 
    return _map(row) if row else None

def get_all() -> list[StudentGroup]: 
    conn = get_connection() 
    cur = conn.cursor() 
    cur.execute(""" SELECT group_id, name, course, faculty FROM student_groups ORDER BY name """) 
    rows = cur.fetchall() 
    conn.close() 
    return [_map(r) for r in rows]

def update(group_id: int, name: str, course: int, faculty: str): 
    conn = get_connection() 
    cur = conn.cursor() 
    cur.execute(""" UPDATE student_groups SET name = ?, course = ?, faculty = ? WHERE group_id = ? """, (name, course, faculty, group_id)) 
    conn.commit() 
    conn.close()

def delete(group_id: int): 
    conn = get_connection() 
    cur = conn.cursor() 
    cur.execute(""" DELETE FROM student_groups WHERE group_id = ? """, (group_id,)) 
    conn.commit() 
    conn.close()