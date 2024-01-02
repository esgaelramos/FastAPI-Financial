"""Routes for API v1."""""

from fastapi import APIRouter

from .endpoints import hello_world, accounts


router = APIRouter()

router.include_router(
    hello_world.router, prefix="", tags=["hello_world"]
)

router.include_router(
    accounts.router, prefix="/auth", tags=["auth_accounts"]
)
