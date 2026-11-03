from dataclasses import dataclass

@dataclass
class User:
    user_id: int
    surname: str
    name: str
    patronymic: str | None
    email: str
    login: str
    password_hash: str 
    role_id: int
    role_name: str | None = None