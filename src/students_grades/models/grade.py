from dataclasses import dataclass

@dataclass
class Grade:
    grade_id: int
    student_id: int
    subject_id: int 
    teacher_id: int
    value: int 
    grade_date: str 
    comment: str | None = None 
    student_name: str | None = None 
    subject_name: str | None = None
    teacher_name: str | None = None