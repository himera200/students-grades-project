from dataclasses import dataclasses


@dataclass
class UserRole:
    role_id int 
    name: str