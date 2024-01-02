"""Tests for Schemas Validating Responses Data."""

from src.schemas.responses_schema import SuccessResponse, ErrorResponse


def test_success_response_validation():
    """Test the SuccessResponse Class."""
    data = {
        "success": True,
        "data": {
            "id": 1,
            "username": "user",
            "email": "ok",
        },
        "message": "Successful Request",
    }
    success_response = SuccessResponse(**data)
    assert success_response.success == data["success"]
    assert success_response.data == data["data"]
    assert success_response.message == data["message"]


def test_error_response_validation():
    """Test the ErrorResponse Class."""
    data = {
        "success": False,
        "message": "Error Request",
    }
    error_response = ErrorResponse(**data)
    assert error_response.success == data["success"]
    assert error_response.message == data["message"]
