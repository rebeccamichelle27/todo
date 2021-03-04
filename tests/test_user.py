from flask import url_for
import pytest

from todo.models import db, User


EXAMPLE_EMAIL = "susan123@example.com"
EXAMPLE_PASSWORD = "123456"

VALID_LOGIN_PARAMS = {
    "email": EXAMPLE_EMAIL,
    "password": EXAMPLE_PASSWORD,
}

VALID_REGISTER_PARAMS = {
    "email": EXAMPLE_EMAIL,
    "password": EXAMPLE_PASSWORD,
    "confirm": EXAMPLE_PASSWORD,
}


def create_user(email=EXAMPLE_EMAIL, password=EXAMPLE_PASSWORD):
    user = User(email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user


def test_user_creation(client, init_database):
    assert User.query.count() == 0
    user = create_user()
    assert User.query.count() == 1
    assert user.password is not EXAMPLE_PASSWORD


def test_username_password_validation(client, init_database):
    assert User.query.count() == 0
    with pytest.raises(ValueError):
        create_user("", EXAMPLE_PASSWORD)
    assert User.query.count() == 0


def test_get_register_route(client, init_database):
    response = client.get(url_for("user.register"))
    assert response.status_code == 200
    assert "Sign up" in str(response.data)
    assert "Email" in str(response.data)
    assert "Confirm Password" in str(response.data)


def test_register(client, init_database):
    response = client.post(
        "/register", data=VALID_REGISTER_PARAMS, follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Registered successfully" in response.data


def test_register_with_existing_user(client, init_database):
    user = create_user()
    response = client.post(
        "/register", data=VALID_REGISTER_PARAMS, follow_redirects=True
    )
    assert response.status_code == 200
    assert b"That email already has an account" in response.data
    assert b"Sign up" in response.data

    assert b"Registered successfully" not in response.data
    assert b"You are already logged in" not in response.data


def test_already_logged_in_register(client, init_database, authenticated_request):
    response = client.post(
        "/register", data=VALID_REGISTER_PARAMS, follow_redirects=True
    )
    assert response.status_code == 200
    assert "You are already logged in" in str(response.data)


def test_get_login_route(client, init_database):
    response = client.get(url_for("user.login"))
    assert response.status_code == 200
    assert "Login" in str(response.data)
    assert "Email" in str(response.data)
    assert "Password" in str(response.data)


def test_login(client, init_database):
    create_user()
    response = client.post(
        url_for("user.login"), data=VALID_LOGIN_PARAMS, follow_redirects=True
    )
    assert response.status_code == 200
    assert b"susan123" in response.data


def test_already_logged_in_login(client, init_database, authenticated_request):
    response = client.post(
        url_for("user.login"), data=VALID_LOGIN_PARAMS, follow_redirects=True
    )

    assert response.status_code == 200
    assert "You are already logged in" in str(response.data)


def test_login_bad_password(client, init_database):
    create_user()
    response = client.post(
        url_for("user.login"),
        data=dict(email=EXAMPLE_EMAIL, password="badpassword"),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "Invalid email or password" in str(response.data)


def test_logout(client, init_database, authenticated_request):
    user = User.query.first()
    response = client.get(url_for("user.logout"), follow_redirects=True)
    assert response.status_code == 200
    assert url_for("user.login") in str(response.data)
    assert url_for("user.logout") not in str(response.data)
    assert b"Log out" not in response.data
