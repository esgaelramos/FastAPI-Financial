"""Schemas for Validating and Standard Responses."""

from pydantic import BaseModel


class SuccessResponse(BaseModel):
    """Validates Successful Responses."""

    success: bool
    data: dict
    message: str = "Successful Request"


class ErrorResponse(BaseModel):
    """Validates Error Responses."""

    success: bool
    message: str
