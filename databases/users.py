from typing import Dict, Optional


class UserMeta:
    def __init__(self, email: str, name: str):
        self.email = email
        self.name = name


__id_pwd: Dict[int, str] = {}
__id_user_meta: Dict[int, UserMeta] = {}


def get_user_by_auth(email: str, password: str) -> Optional[UserMeta]:
    for (id, user_meta) in __id_user_meta.items():
        if user_meta.email == email:
            if __id_pwd[id] != password:
                return None
            return user_meta
    return None


def is_email_occupied(email: str) -> bool:
    for (_, user_meta) in __id_user_meta.items():
        if user_meta.email == email:
            return True
    return False


def add_user(email: str, name: str, password: str):
    if is_email_occupied(email):
        raise ValueError("User with this email exists")
    id = len(__id_pwd)
    __id_pwd[id] = password
    __id_user_meta[id] = UserMeta(email, name)


def get_num_of_users():
    return len(__id_user_meta)