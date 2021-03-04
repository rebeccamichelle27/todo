import pytest
from flask import url_for
from todo.models import User


def test_guest_index_page(client, init_database):
    response = client.get(url_for("landing.index"))
    assert response.status_code == 200
    assert b"Please register or log in" in response.data
    assert b"To do:" not in response.data


def test_logged_in_index_page(client, init_database, authenticated_request):
    authed_user = User.query.all()[0]
    response = client.get(url_for("landing.index"))

    assert response.status_code == 200
    assert b"Welcome, susan123@example.com" in response.data
    assert b"To do:" in response.data


def test_add_todo(client, init_database, authenticated_request):
    response = client.post(
        url_for("landing.index"), data=dict(todo="clean"), follow_redirects=True
    )
    print(response.data)
    assert response.status_code == 200
    assert b"clean" in response.data
