import pytest
from utils import validate_new_password
from databases.users import add_user, get_user_by_auth
from pydantic import SecretStr


# ~~~~~~~~~~~~~~~~~ validate password tests ~~~~~~~~~~~~~~~~~~~~
def test_correct_password():
    validate_new_password(SecretStr("Ab1!"))


def test_miss_lowercase():
    with pytest.raises(ValueError) as ve:
        validate_new_password(SecretStr("A1!"))
    assert ve.value.args[1] == r"[a-z]"


def test_miss_uppercase():
    with pytest.raises(ValueError) as ve:
        validate_new_password(SecretStr("b1!"))
    assert ve.value.args[1] == r"[A-Z]"


def test_miss_digit():
    with pytest.raises(ValueError) as ve:
        validate_new_password(SecretStr("Ab!"))
    assert ve.value.args[1] == r"[0-9]"


def test_miss_special_char():
    with pytest.raises(ValueError) as ve:
        validate_new_password(SecretStr("Ab1"))
    assert ve.value.args[1] == r"[!@#_.]"


def test_wrong_char():
    with pytest.raises(ValueError) as ve:
        validate_new_password(SecretStr("Ab1!$"))
    assert ve.value.args[1] == "wrong char"


@pytest.fixture()
def setup_and_teardown_db():
    from databases.users import __id_pwd, __id_user_meta
    save_pwd = __id_pwd.copy()
    save_meta = __id_user_meta.copy()
    __id_pwd.clear()
    __id_user_meta.clear()

    __id_pwd = save_pwd
    __id_user_meta = save_meta


# ~~~~~~~~~~~~~~~~~ add new user tests ~~~~~~~~~~~~~~~~~~~~
def test_add_user_correct_params(setup_and_teardown_db):
    add_user(email="a@yandex.ru", name="a", password="Aa1!")
    add_user(email="b@yandex.ru", name="b", password="Bb2@")


def test_add_user_with_existing_name(setup_and_teardown_db):
    add_user(email="a@yandex.ru", name="a", password="Aa1!")
    add_user(email="b@yandex.ru", name="a", password="Aa1!")


def test_add_user_occupied_email(setup_and_teardown_db):
    add_user(email="a@yandex.ru", name="a", password="Aa1!")
    with pytest.raises(ValueError):
        add_user(email="a@yandex.ru", name="b", password="Bb2@")


# # ~~~~~~~~~~~~~~~~~ get user meta tests ~~~~~~~~~~~~~~~~~~~~
def test_get_user_meta_correct_params(setup_and_teardown_db):
    add_user(email="a@yandex.ru", name="a", password="Aa1!")
    assert get_user_by_auth(email="a@yandex.ru", password="Aa1!") is not None


def test_get_user_meta_occupied_email(setup_and_teardown_db):
    add_user(email="a@yandex.ru", name="a", password="Aa1!")
    assert get_user_by_auth(email="aa@yandex.ru", password="Aa1!") is None


def test_get_user_meta_wrong_password(setup_and_teardown_db):
    add_user(email="a@yandex.ru", name="a", password="Aa1!")
    assert get_user_by_auth(email="a@yandex.ru", password="Aa1!!") is None
