"""EndPoints for Belvo Links."""""

from typing import Optional

from requests import HTTPError
from fastapi import APIRouter, HTTPException, Depends
from src.belvo.instance import get_belvo_client
from src.schemas.responses_schema import SuccessResponse


router = APIRouter()


@router.get("/links")
async def get_belvo_links(
    client = Depends(get_belvo_client), id: Optional[str] = None  # noqa: E251
):
    """Get Belvo Links EndPoint. All Links or a specific Link by ID."""
    try:
        # Get the Belvo Links Resource
        links_resource = client.Links

        if id:
            try:
                data = links_resource.get(id)
            except HTTPError as http_err:
                raise HTTPException(
                    status_code=http_err.response.status_code,
                    detail=http_err.response.json()
                )
        else:
            # Convert Generator to a List of Dictionaries
            list_links = list(links_resource.list())
            data = {"links": list_links}

        return SuccessResponse(
            success=True,
            message="Belvo Links",
            data=data
        ).model_dump()

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )
