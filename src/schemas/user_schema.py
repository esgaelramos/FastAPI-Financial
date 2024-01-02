"""Schemas for Validating User Data."""

from pydantic import BaseModel, EmailStr


class UserRequest(BaseModel):
    """Validates User Data Input."""

    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Validates User Data Output."""

    username: str
    email: EmailStr


class UserTokenResponse(BaseModel):
    """Validates User Token Data Output."""

    username: str
    email: EmailStr
    access_token: str
    token_type: str = "bearer"
