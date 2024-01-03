"""Module `auth` for all the accounts logic."""

import logging
from datetime import datetime, timedelta

from decouple import config
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from src.models.user import User
from src.schemas.user_schema import UserRequest


ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = config('SECRET_KEY', 'ACCESS_SECRET_KEY')


class AuthHandler:
    """Class for the authentication logic."""

    def __init__(self):
        """Initialize the database."""
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(
            self, plain_password: str, hashed_password: str) -> bool:
        """Compare a plain password with a hashed password."""
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """Obtain the hash of a password."""
        return self.pwd_context.hash(password)

    def create_access_token(self, data: dict) -> str:
        """Create a JWT for access token.

        Give an expiration time of 30 minutes.
        Update the data with the expiration time.
        """
        payload = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
        payload.update({"exp": expire})
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    def decode_access_token(self, token: str) -> dict:
        """Decode a JWT access token."""
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError as e:
            logging.error(e)
            return None


# Create an instance of the class
auth = AuthHandler()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/auth/token")


def get_user_by_username(username: str, db: Session) -> User:
    """Get a user with username from the database.

    Args:
        username (str): Username.
        db (Session): Database Session.

    Returns:
        User: Model User.
    """
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(email: str, db: Session) -> User:
    """Get a user with email from the database.

    Args:
        email (str): Email.
        db (Session): Database Session.

    Returns:
        User: Model User.
    """
    return db.query(User).filter(User.email == email).first()


def register_new_user(user_data: UserRequest, db: Session) -> User:
    """Register a new user in the database.

    Before register a new user, check if the username or email already exists.

    Args:
        user_data (UserRequest): User Data.
        db (Session): Database Session.

    Returns:
        User: Model User.
    """
    if get_user_by_username(user_data.username, db)\
            or get_user_by_email(user_data.email, db):
        raise HTTPException(
            status_code=400, detail="Username or email already in use"
        )

    hashed_password = auth.get_password_hash(user_data.password)
    new_user = User(username=user_data.username,
                    email=user_data.email,
                    hashed_password=hashed_password)

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        logging.error(e)
        db.rollback()
        return None

    if new_user is None:
        raise HTTPException(
            status_code=500, detail="Error registering new user"
        )

    return new_user


def authenticate_user(username: str, password: str, db: Session) -> User:
    """Authenticate a user with a username and password.

    Args:
        username (str): Username.
        password (str): Password.
        db (Session): Database Session.

    Returns:
        User: Model User.
    """
    user = get_user_by_username(username, db)
    if not user or not auth.verify_password(password, user.hashed_password):  # noqa: E501
        raise HTTPException(
            status_code=401, detail="Incorrect username or password"
        )
    return user


def get_current_user(token: str, db: Session) -> User:
    """Get the current user from the database.

    Args:
        token (str): JWT Token.
        db (Session): Database Session.

    Returns:
        User: Model User.
    """
    payload = auth.decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user
