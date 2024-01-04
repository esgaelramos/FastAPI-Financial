"""EndPoints for Belvo Accounts."""""

from typing import Optional

from requests import HTTPError
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.core.auth import oauth2_scheme
from src.core.database import get_session
from src.belvo.instance import get_belvo_client
from src.schemas.responses_schema import SuccessResponse


router = APIRouter()


@router.get("/accounts")
async def get_belvo_accounts(
    id: Optional[str] = None, client = Depends(get_belvo_client),  # noqa: E251
    db: Session = Depends(get_session), token: str = Depends(oauth2_scheme)
):
    """Get Belvo Accounts EndPoint. All Accounts or specific Account by ID."""
    try:
        # Get the Belvo Accounts Resource
        accounts_resource = client.Accounts

        if id:
            try:
                data = accounts_resource.get(id)
            except HTTPError as http_err:
                raise HTTPException(
                    status_code=http_err.response.status_code,
                    detail=http_err.response.json()
                )
        else:
            # Convert Generator to a List of Dictionaries
            list_accounts = list(accounts_resource.list())
            data = {"accounts": list_accounts}

        return SuccessResponse(
            success=True,
            message="Belvo Accounts",
            data=data
        ).model_dump()

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )
