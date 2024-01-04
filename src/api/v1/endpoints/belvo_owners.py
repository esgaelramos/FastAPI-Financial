"""EndPoints for Belvo Ownwers."""""

from typing import Optional

from requests import HTTPError
from fastapi import APIRouter, HTTPException, Depends
from src.belvo.instance import get_belvo_client
from src.schemas.responses_schema import SuccessResponse


router = APIRouter()


@router.get("/owners")
async def get_belvo_owners(
    client = Depends(get_belvo_client), id: Optional[str] = None  # noqa: E251
):
    """Get Belvo Owners EndPoint. All Owners or a specific Owner by ID."""
    try:
        # Get the Belvo Owners Resource
        owners_resource = client.Owners

        if id:
            try:
                data = owners_resource.get(id)
            except HTTPError as http_err:
                raise HTTPException(
                    status_code=http_err.response.status_code,
                    detail=http_err.response.json()
                )
        else:
            # Convert Generator to a List of Dictionaries
            list_owners = list(owners_resource.list())
            data = {"owners": list_owners}

        return SuccessResponse(
            success=True,
            message="Belvo Owners",
            data=data
        ).model_dump()

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )
