"""Routes for API v1."""""

from fastapi import APIRouter

from .endpoints import (
    accounts, belvo_links, hello_world
)


router = APIRouter()

router.include_router(
    hello_world.router, prefix="", tags=["hello_world"]
)

router.include_router(
    accounts.router, prefix="/auth", tags=["auth_accounts"]
)

router.include_router(
    belvo_links.router, prefix="/belvo", tags=["belvo_links"]
)
