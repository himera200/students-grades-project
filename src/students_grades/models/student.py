from dataclasses import dataclass


@dataclass
class Student:
    student_id: int
    user_id: int
    group_id: int 
    record_book_number: str
    full_name: str | None = None
    group_name: str | None = None
    