"""EndPoints for Belvo Transactions."""""

from typing import Optional

from requests import HTTPError
from fastapi import APIRouter, HTTPException, Depends
from src.core.auth import oauth2_scheme
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


@router.get("/transactions-outcomes/")
async def get_belvo_transactions_out(
    client = Depends(get_belvo_client), token: str = Depends(oauth2_scheme),  # noqa: E501,E251
    link: str = None, account: str = None, page: Optional[int] = 1
):
    """Get Mounts of All Belvo Outcomes Transactions By Category EndPoint."""
    try:
        transactions_resource = client.Transactions
        try:
            list_transactions = list(transactions_resource.list(
                page=page, account=account, link=link
            ))
            grouped_data = \
                group_mount_transactions(list_transactions, "OUTFLOW")
            data = {"transactions_by_category": grouped_data}

        except HTTPError as http_err:
            raise HTTPException(
                status_code=http_err.response.status_code,
                detail=http_err.response.json()
            )
        return SuccessResponse(
            success=True,
            message="Belvo Transactions Mounts Outcomes",
            data=data
        ).model_dump()

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


@router.get("/transactions-incomes/")
async def get_belvo_transactions_in(
    client = Depends(get_belvo_client), token: str = Depends(oauth2_scheme),  # noqa: E501,E251
    link: str = None, account: str = None, page: Optional[int] = 1
):
    """Get Mounts of All Belvo Incomes Transactions By Category EndPoint."""
    try:
        transactions_resource = client.Transactions
        try:
            list_transactions = list(transactions_resource.list(
                page=page, account=account, link=link
            ))
            grouped_data = \
                group_mount_transactions(list_transactions, "INFLOW")
            data = {"transactions_by_category": grouped_data}

        except HTTPError as http_err:
            raise HTTPException(
                status_code=http_err.response.status_code,
                detail=http_err.response.json()
            )
        return SuccessResponse(
            success=True,
            message="Belvo Transactions Mounts Incomes",
            data=data
        ).model_dump()

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


def group_mount_transactions(transactions, type_transaction="OUTFLOW"):
    """Group Transactions by Category.

    This function is used to group transactions by category.
    Transactions are filtered by type of transaction (INFLOW or OUTFLOW).

    Args:
        transactions (list): List of Belvo Transactions.
        type_transaction (str): Type of Transaction. (INFLOW or OUTFLOW)

    Returns:
        dict: Grouped Transactions by Category.
    """
    grouped_data = {}
    for transaction in transactions:
        if transaction.get("type") == type_transaction:
            category = transaction.get("category", "Uncategorized")
            amount = transaction.get("amount", 0)

            grouped_data[category] = \
                grouped_data.get(category, 0) + amount

    return grouped_data
