"""EndPoints for Belvo Transactions."""""

from typing import Optional

from requests import HTTPError
from fastapi import APIRouter, HTTPException, Depends
from src.belvo.instance import get_belvo_client
from src.schemas.responses_schema import SuccessResponse


router = APIRouter()


@router.get("/transactions/")
async def get_belvo_transactions(
    client = Depends(get_belvo_client), link: str = None,  # noqa: E251
    account: str = None, page: Optional[int] = 1
):
    """Get Belvo Transactions EndPoint. List all Transactions.

    This EndPoint is used to get a list of Belvo Transactions.
    The list of transactions need to be filtered by account and link.
    And for a better performance, the list is paginated.
    """
    try:
        # Get the Belvo Transactions Resource
        transactions_resource = client.Transactions

        try:
            # Convert Generator to a List of Dictionaries
            list_transactions = list(transactions_resource.list(
                page=page, account=account, link=link
            ))
            data = {"transactions": list_transactions}
        except HTTPError as http_err:
            raise HTTPException(
                status_code=http_err.response.status_code,
                detail=http_err.response.json()
            )
        return SuccessResponse(
            success=True,
            message="Belvo Transactions",
            data=data
        ).model_dump()

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )
