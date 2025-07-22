# app/models/user.py
from datetime import datetime, timedelta
import uuid
from typing import Optional, Dict, Any

from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship
from passlib.context import CryptContext
from jose import JWTError, jwt
from pydantic import ValidationError

from app.schemas.base import UserCreate
from app.schemas.user import UserResponse, Token

from app.database import Base


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Move to config
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(50), default="", nullable=False)
    last_name = Column(String(50), default="", nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    # Provide backward compatibility for using `password` in constructors
    @property
    def password(self) -> str:
        return self.password_hash

    @password.setter
    def password(self, value: str) -> None:
        self.password_hash = value
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    calculations = relationship("Calculation", back_populates="user")

    def __repr__(self):
        return f"<User(name={self.first_name} {self.last_name}, email={self.email})>"

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt."""
        return pwd_context.hash(password)
    
    def set_password(self, raw_password: str) -> None:
        """Hash and store a new password."""
        self.password_hash = self.hash_password(raw_password)

    def verify_password(self, plain_password: str) -> bool:
        """Verify a plain password against the stored password hash."""
        return pwd_context.verify(plain_password, self.password_hash)

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token."""
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def verify_token(token: str) -> Optional[UUID]:
        """Verify and decode a JWT token."""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("sub")
            return uuid.UUID(user_id) if user_id else None
        except (JWTError, ValueError):
            return None

    @classmethod
    def register(cls, db, user_data: Dict[str, Any]) -> "User":
        """Register a new user with validation."""
        try:
            # Validate password length first
            password = user_data.get('password', '')
            if len(password) < 6:  # Strictly less than 6 characters
                raise ValueError("Password must be at least 6 characters long")
            
            # Check if email/username exists
            existing_user = db.query(cls).filter(
                (cls.email == user_data.get('email')) |
                (cls.username == user_data.get('username'))
            ).first()
            
            if existing_user:
                raise ValueError("Username or email already exists")

            # Validate using Pydantic schema
            user_create = UserCreate.model_validate(user_data)
            
            # Create new user instance
            new_user = cls(
                first_name=user_data.get("first_name", ""),
                last_name=user_data.get("last_name", ""),
                email=user_create.email,
                username=user_create.username,
                password_hash=cls.hash_password(user_create.password),
                is_active=True,
                is_verified=False
            )
            
            db.add(new_user)
            db.flush()
            return new_user
            
        except ValidationError as e:
            raise ValueError(str(e)) # pragma: no cover
        except ValueError as e:
            raise e

    @classmethod
    def authenticate(cls, db, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user and return token with user data."""
        user = db.query(cls).filter(
            (cls.username == username) | (cls.email == username)
        ).first()

        if not user or not user.verify_password(password):
            return None # pragma: no cover

        user.last_login = datetime.utcnow()
        db.commit()

        # Create token response using Pydantic models
        user_response = UserResponse.model_validate(user)
        token_response = Token(
            access_token=cls.create_access_token({"sub": str(user.id)}),
            token_type="bearer",
            user=user_response
        )

        return token_response.model_dump()