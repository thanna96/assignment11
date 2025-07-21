import pytest
from sqlalchemy.exc import IntegrityError
from app.models.user import User


def test_unique_constraints(db_session):
    user1 = User(username="unique", email="unique@example.com", password_hash=User.hash_password("pass"))
    db_session.add(user1)
    db_session.commit()

    user2 = User(username="unique", email="other@example.com", password_hash=User.hash_password("pass"))
    db_session.add(user2)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_invalid_email_registration(db_session):
    data = {"username": "bad", "email": "not-an-email", "password": "pass123"}
    with pytest.raises(ValueError):
        User.register(db_session, data)