from dataclasses import dataclass

@dataclass
class Teacher:
    teacher_id: int
    user_id: int 
    department: str 
    full_name: str | None = None