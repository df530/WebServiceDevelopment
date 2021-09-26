from pydantic import SecretStr
import re


def validate_new_password(pwd: SecretStr):
    value = pwd.get_secret_value()
    if re.search(r"[a-z]", value) is None:
        raise ValueError("password must contain lowercase letter", r"[a-z]")
    if re.search(r"[A-Z]", value) is None:
        raise ValueError("password must contain uppercase letter", r"[A-Z]")
    if re.search(r"[0-9]", value) is None:
        raise ValueError("password must contain digit", r"[0-9]")
    if re.search(r"[!@#_.]", value) is None:
        raise ValueError("password must contain special character '!', '@', '#', '_' or '.'", r"[!@#_.]")
    m = re.search(r"[^a-zA-Z0-9!@#_.]", value)
    if m is not None:
        raise ValueError("password contains forbidden character " + m.group(0), "wrong char")
