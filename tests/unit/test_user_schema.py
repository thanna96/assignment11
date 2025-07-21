import pytest
from pydantic import ValidationError
from app.schemas.user import UserCreate, UserRead
from uuid import uuid4
from datetime import datetime


def test_user_create_valid():
    data = {"username": "john", "email": "john@example.com", "password": "pass123"}
    user = UserCreate(**data)
    assert user.username == "john"
    assert user.email == "john@example.com"


def test_user_create_invalid_email():
    with pytest.raises(ValidationError):
        UserCreate(username="john", email="bad-email", password="pass123")


def test_user_read_model():
    user = UserRead(id=uuid4(), username="u", email="e@example.com", created_at=datetime.utcnow())
    assert user.email == "e@example.com"