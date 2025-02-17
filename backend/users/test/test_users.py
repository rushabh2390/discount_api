import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from databases.database import data
from users.routers.users import get_password_hash, create_access_token, verify_password,  generate_discount_code
from config.config import settings
from main import app

client = TestClient(app)

# Helper function to create a test user


def create_test_user(email, password, is_admin=False, username="testuser"):
    user_data = {
        "email": email,
        "password": get_password_hash(password),
        "username": "testuser",
        "date_of_birth": "2000-10-10",
        "fullname": "New User",
        "isstaffuser": False,
        "isadminuser": is_admin
    }
    data.users[email] = user_data
    return user_data

# Helper function to get access token


def get_access_token(email, password):
    form_data = OAuth2PasswordRequestForm(
        grant_type="password", username=email, password=password)
    response = client.post("/users/login", data=form_data.__dict__)
    return response.json()["access_token"]


def test_create_user():
    user_data = {
        "email": "newuser@example.com",
        "password": get_password_hash("password123"),
        "username": "newuser",
        "date_of_birth": "2000-10-10",
        "fullname": "New User",
        "isstaffuser": False,
        "isadminuser": False
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    user_data = response.json()
    assert user_data["email"] == "newuser@example.com"

    # Test for duplicate user
    response = client.post("/users/", json=user_data)
    assert response.status_code == 409
    assert response.json()[
        "detail"] == "User with existing email is already exist"


def test_read_user():
    create_test_user("test@example.com", "password123")
    response = client.get("/users/test@example.com")
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

    response = client.get("/users/nonexistent@example.com")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_login_user():
    create_test_user("login@example.com", "password123")
    form_data = OAuth2PasswordRequestForm(
        grant_type="password", username="login@example.com", password="password123")
    response = client.post("/users/login", data=form_data.__dict__)
    assert response.status_code == 200
    assert "access_token" in response.json()

    form_data = OAuth2PasswordRequestForm(grant_type="password",
                                          username="login@example.com", password="wrongpassword")
    response = client.post("/users/login", data=form_data.__dict__)
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email/username or password"


def test_read_users_me():
    create_test_user("me@example.com", "password123")
    token = get_access_token("me@example.com", "password123")
    response = client.get(
        "/users/about_me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["email"] == "me@example.com"

    token = get_access_token("me@example.com", "password123")
    del data.users["me@example.com"]
    response = client.get(
        "/users/about_me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_generate_discount():
    create_test_user("admin@example.com", "password123", is_admin=True)
    admin_token = get_access_token("admin@example.com", "password123")
    response = client.get("/users/generate_discount",
                          headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert "coupon_code" in response.json()

    create_test_user("user@example.com", "password123", is_admin=False)
    user_token = get_access_token("user@example.com", "password123")
    response = client.get("/users/generate_discount",
                          headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 403
    assert response.json()["detail"] == "Only admin can generate discount"
