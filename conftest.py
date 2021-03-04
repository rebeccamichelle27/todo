import pytest
from flask import url_for

from todo import create_app
from todo.extensions import db
from todo.models import User, Todo


@pytest.fixture
def app():
    return create_app("test")


@pytest.fixture
# Create the database
def init_database():
    db.create_all()
    yield
    db.drop_all()


@pytest.fixture
# Create a user and log them in
def authenticated_request(client):
    new_user = User(email="susan123@example.com")
    new_user.set_password("123456")
    db.session.add(new_user)
    db.session.commit()

    response = client.post(
        url_for("user.login"),
        data={"email": "susan123@example.com", "password": "123456"},
        follow_redirects=True,
    )
    yield client
