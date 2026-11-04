from src.students_grades.database.database import get_connection
from src.students_grades.models.subject import Subject

def _map(row) -> Subject: 
    return Subject(*row)

def create(name: str, hours: int, semester: int): 
    conn = get_connection()
    cur = conn.cursor() 
    cur.execute(""" INSERT INTO subjects (name, hours, semester) VALUES (?, ?, ?) """, (name, hours, semester)) 
    conn.commit() 
    conn.close()

def get_by_id(subject_id: int) -> Subject | None: 
    conn = get_connection() 
    cur = conn.cursor() 
    cur.execute(""" SELECT subject_id, name, hours, semester FROM subjects WHERE subject_id = ? """, (subject_id,)) 
    row = cur.fetchone() 
    conn.close() 
    return _map(row) if row else None

def get_all() -> list[Subject]: 
    conn = get_connection() 
    cur = conn.cursor() 
    cur.execute(""" SELECT subject_id, name, hours, semester FROM subjects ORDER BY name """) 
    rows = cur.fetchall() 
    conn.close() 
    return [_map(r) for r in rows]

def update(subject_id: int, name: str, hours: int, semester: int): 
    conn = get_connection() 
    cur = conn.cursor() 
    cur.execute(""" UPDATE subjects SET name = ?, hours = ?, semester = ? WHERE subject_id = ? """, (name, hours, semester, subject_id)) 
    conn.commit() 
    conn.close()

def delete(subject_id: int): 
    conn = get_connection() 
    cur = conn.cursor() 
    cur.execute(""" DELETE FROM subjects WHERE subject_id = ? """, (subject_id,)) 
    conn.commit() 
    conn.close()