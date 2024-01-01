"""EndPoints for Hello World."""""

from fastapi import APIRouter


router = APIRouter()


@router.get("/")
async def hello_world():
    """Hello World EndPoint."""
    return {"from Hello World": "to FastAPI-Financial"}
