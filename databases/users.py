from typing import Dict, Optional
from datetime import date


class UserMeta:
    class AdditionalInfo:
        status: Optional[str]
        birth_date: Optional[date]

        def __init__(self, status: Optional[str] = None, birth_date: Optional[date] = None):
            self.status = status
            self.birth_date = birth_date

    email: str
    name: str
    additional_info: AdditionalInfo

    def __init__(self, email: str, name: str, additional_info: AdditionalInfo = AdditionalInfo()):
        self.email = email
        self.name = name
        self.additional_info = additional_info


__id_pwd: Dict[int, str] = {}
__id_user_meta: Dict[int, UserMeta] = {}
__email_id: Dict[str, int] = {}


def get_user_by_auth(email: str, password: str) -> Optional[UserMeta]:
    if not is_email_occupied(email):
        return None
    id = __email_id[email]
    if __id_pwd[id] != password:
        return None
    return __id_user_meta[id]


def is_email_occupied(email: str) -> bool:
    return email in __email_id


def add_user(email: str, name: str, password: str):
    if is_email_occupied(email):
        raise ValueError("User with this email exists")
    id = len(__id_pwd)
    __id_pwd[id] = password
    __id_user_meta[id] = UserMeta(email, name)
    __email_id[email] = id


def get_num_of_users():
    return len(__id_user_meta)
