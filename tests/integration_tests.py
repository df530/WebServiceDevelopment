import pytest
from fastapi.testclient import TestClient

from main import datagram_app

client = TestClient(datagram_app)


@pytest.fixture()
def setup_and_teardown_db():
    from databases.users import __id_pwd, __id_user_meta
    save_pwd = __id_pwd.copy()
    save_meta = __id_user_meta.copy()
    __id_pwd.clear()
    __id_user_meta.clear()

    __id_pwd = save_pwd
    __id_user_meta = save_meta


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ registration test ~~~~~~~~~~~~~~~~~~
def test_registration_success(setup_and_teardown_db):
    rs = client.post("/users/registration", json={"email": "a@yandex.ru", "name": "a", "password": "Aa1!"})
    assert rs.status_code == 201


def test_registration_wrong_pwd_format(setup_and_teardown_db):
    rs = client.post("/users/registration", json={"email": "a@yandex.ru", "name": "a", "password": "a1!"})
    assert rs.status_code == 422


def test_registration_mail_occupied(setup_and_teardown_db):
    rs = client.post("/users/registration", json={"email": "a@yandex.ru", "name": "a", "password": "Aa1!"})
    assert rs.status_code == 201
    rs = client.post("/users/registration", json={"email": "a@yandex.ru", "name": "a", "password": "Aa1!"})
    assert rs.status_code == 403


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ auth test ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def test_auth_success(setup_and_teardown_db):
    rs = client.post("/users/registration", json={"email": "a@yandex.ru", "name": "a", "password": "Aa1!"})
    assert rs.status_code == 201
    rs = client.post("/users/auth", json={"email": "a@yandex.ru", "password": "Aa1!"})
    assert rs.status_code == 200


def test_auth_user_not_exist(setup_and_teardown_db):
    rs = client.post("/users/registration", json={"email": "a@yandex.ru", "name": "a", "password": "Aa1!"})
    assert rs.status_code == 201
    rs = client.post("/users/auth", json={"email": "b@yandex.ru", "password": "Aa1!"})
    assert rs.status_code == 403


def test_auth_wrong_password(setup_and_teardown_db):
    rs = client.post("/users/registration", json={"email": "a@yandex.ru", "name": "a", "password": "Aa1!"})
    assert rs.status_code == 201
    rs = client.post("/users/auth", json={"email": "a@yandex.ru", "password": "Ba1!"})
    assert rs.status_code == 403
