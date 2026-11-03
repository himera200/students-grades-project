from dataclasses import dataclass


@dataclass
class StudentGroup:
    group_id: int
    name: str
    hours: int
    semester: int 