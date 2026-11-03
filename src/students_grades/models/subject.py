from dataclasses import dataclass


@dataclass
class Subject:
    subject_id: int
    name: str
    hours: int
    semester: int 