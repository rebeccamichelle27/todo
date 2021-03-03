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
    new_user = User(username="susan123")
    new_user.set_password("123456")
    db.session.add(new_user)
    db.session.commit()

    response = client.post(
        url_for("user.login"),
        # not sure how to update the password below to make sure it matches the hashed one
        data={"username": "susan123", "password": "123456"},
        follow_redirects=True,
    )
    yield client
