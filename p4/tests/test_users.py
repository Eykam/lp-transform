from flask import session, request
import pytest

from types import SimpleNamespace

from flask_app.forms import RegistrationForm
from flask_app.models import User


def test_register(client, auth):
    """ Test that registration page opens up """
    resp = client.get("/register")
    assert resp.status_code == 200

    response = auth.register()

    assert response.status_code == 200
    user = User.objects(username="test").first()

    assert user is not None


@pytest.mark.parametrize(
    ("username", "email", "password", "confirm", "message"),
    (
        ("test", "test@email.com", "test", "test", b"Username is taken"),
        ("p" * 41, "test@email.com", "test", "test", b"Field must be between 1 and 40"),
        ("username", "test", "test", "test", b"Invalid email address."),
        ("username", "test@email.com", "test", "test2", b"Field must be equal to"),
    ),
)
def test_register_validate_input(auth, username, email, password, confirm, message):
    if message == b"Username is taken":
        auth.register()

    response = auth.register(username, email, password, confirm)

    assert message in response.data


def test_login(client, auth):
    """ Test that login page opens up """
    resp = client.get("/login")
    assert resp.status_code == 200

    auth.register()
    response = auth.login()

    with client:
        client.get("/")
        assert session["_user_id"] == "test"


@pytest.mark.parametrize(("username", "password", "message"), ())
def test_login_input_validation(auth, username, password, message):
    assert False


def test_logout(client, auth):
    #testing reg and login
    resp = client.get("/register")
    assert resp.status_code == 200   # good if we get status code 200 (OK)
    auth.register()
    response = auth.login()
    assert response.status_code == 200
    response_logout = auth.logout()
    assert response_logout.status_code == 302


def test_change_username(client, auth):
    assert False


def test_change_username_taken(client, auth):
    # Register two users
    auth.register(username='user1', email="test1@test.com")
    auth.register(username='user2', email="test2@test.com")
    
    # Log in as the first user
    resp = auth.login(username='user1')
    assert resp.status_code == 200

    # Attempt to change the username to the second user's username
    response = client.post('/account', data={'Username': 'user2'}, follow_redirects=True)
    print(response)
    # Check that the response contains the expected error message
    #assert b"Username is taken" in response.data
    
    user = User.objects(username='user1').first()
    print(user)
    assert user


@pytest.mark.parametrize(
    ("new_username",), 
    (
    )
)
def test_change_username_input_validation(client, auth, new_username):
    assert False

        
 
