from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest
from app.security.jwt import create_access_token
from app.security.password import hash_password, verify_password


class AuthError(Exception):
    """Base authentication error."""


class UserAlreadyExistsError(AuthError):
    """Raised when email or username already exists."""


class InvalidCredentialsError(AuthError):
    """Raised when login credentials are invalid."""


def register_user(
    db: Session,
    data: RegisterRequest,
) -> User:
    existing_email = db.scalar(
        select(User).where(User.email == data.email)
    )

    if existing_email is not None:
        raise UserAlreadyExistsError("Email already registered")

    existing_username = db.scalar(
        select(User).where(User.username == data.username)
    )

    if existing_username is not None:
        raise UserAlreadyExistsError("Username already registered")

    user = User(
        email=data.email,
        username=data.username,
        password_hash=hash_password(data.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(
    db: Session,
    data: LoginRequest,
) -> User:
    user = db.scalar(
        select(User).where(User.email == data.email)
    )

    if user is None:
        raise InvalidCredentialsError("Invalid email or password")

    if not verify_password(data.password, user.password_hash):
        raise InvalidCredentialsError("Invalid email or password")

    return user


def create_user_token(user: User) -> str:
    return create_access_token(
        data={
            "sub": str(user.id),
            "email": user.email,
        },
        secret_key=settings.jwt_secret_key,
    )
