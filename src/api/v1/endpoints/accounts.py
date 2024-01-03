"""EndPoints for Auth Accounts."""""

from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from src.core.auth import (
    auth, oauth2_scheme,
    register_new_user, authenticate_user, get_current_user
)
from src.schemas.user_schema import (
    UserRequest, UserResponse, UserTokenResponse
)
from src.schemas.responses_schema import SuccessResponse
from src.core.database import get_session

router = APIRouter()


@router.post("/register", response_model=UserTokenResponse)
async def register(user_data: UserRequest, db: Session = Depends(get_session)):
    """Register a New User Endpoint.

    This endpoint will register a new user and return a JWT token.
    """
    new_user = register_new_user(user_data, db)

    access_token = auth.create_access_token(data={"sub": new_user.username})
    return UserTokenResponse(
        username=new_user.username,
        email=new_user.email,
        access_token=access_token
    )


@router.post("/login", response_model=UserTokenResponse)
async def login(user_credentials: UserRequest,
                db: Session = Depends(get_session)):
    """Login User with Credentials Endpoint.

    This endpoint will login a user with credentials and return a JWT token.
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


@router.post("/token")
async def token(user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()],  # noqa: E501
                db: Session = Depends(get_session)):
    """Get JWT Token Endpoint."""
    user = authenticate_user(
        user_credentials.username, user_credentials.password, db
    )

    access_token = auth.create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=UserResponse)
async def read_current_user(db: Session = Depends(get_session),
                            token: str = Depends(oauth2_scheme)):
    """Endpoint to get current user information.

    This endpoint will return the current user information.
    For this, the user must be authenticated and send a valid JWT token.
    The token must be sent in the Authorization header as a Bearer token.
    """
    user = get_current_user(token, db)

    return UserResponse(
        username=user.username,
        email=user.email
    )


@router.get("/need-auth", response_model=SuccessResponse)
async def need_auth(db: Session = Depends(get_session),
                    token: str = Depends(oauth2_scheme)):
    """Need Auth for Access EndPoint."""
    user = get_current_user(token, db)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return {"success": True, "data": {"message": "Authorized Access"}}
