"""Schemas for Validating User Data."""

from pydantic import BaseModel, EmailStr


class UserRequest(BaseModel):
    """Validates User Data Input."""

    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Validates User Data Output."""

    id: int
    username: str
    email: EmailStr
