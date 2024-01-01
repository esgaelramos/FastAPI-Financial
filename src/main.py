"""Main module for the FastAPI-Financial application."""

from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def hello_world():
    """Hello World EndPoint."""
    return {"from Hello World": "to FastAPI-Financial"}
