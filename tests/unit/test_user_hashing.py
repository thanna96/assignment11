import pytest
from app.models.user import User


def test_password_hash_and_verify():
    raw = "SecurePass123"
    hashed = User.hash_password(raw)
    assert hashed != raw
    user = User(username="tester", email="t@example.com", password_hash=hashed)
    assert user.verify_password(raw)
    assert not user.verify_password("wrong")