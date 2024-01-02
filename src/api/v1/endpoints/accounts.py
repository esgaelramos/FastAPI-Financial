"""EndPoints for Auth Accounts."""""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.core.auth import auth, register_new_user, authenticate_user
from src.schemas.user_schema import UserRequest, UserTokenResponse
from src.core.database import get_session

router = APIRouter()


@router.post("/register", response_model=UserTokenResponse)
async def register(user_data: UserRequest, db: Session = Depends(get_session)):
    """Register a New User Endpoint.

    This endpoint will register a new user and return a JWT token.

    Args:
        user_data (UserRequest): User Data.
        db (Session, optional): Database Session.

    Returns:
        UserTokenResponse: User Data and JWT Token.
    """
    new_user = register_new_user(user_data, db)

    access_token = auth.create_access_token(data={"sub": new_user.username})
    return UserTokenResponse(
        username=new_user.username,
        email=new_user.email,
        access_token=access_token
    )


@router.post("/login", response_model=UserTokenResponse)
async def login(user_credentials: UserRequest, db: Session = Depends(get_session)):  # noqa: E501
    """Login User with Credentials Endpoint.

    This endpoint will login a user with credentials and return a JWT token.

    Args:
        user_credentials (UserRequest): User Credentials.
        db (Session, optional): Database Session.

    Returns:
        UserTokenResponse: User Data and JWT Token.
    """
    user = authenticate_user(
        user_credentials.username, user_credentials.password, db
    )

    access_token = auth.create_access_token(data={"sub": user.username})
    return UserTokenResponse(
        username=user.username,
        email=user.email,
        access_token=access_token
    )
