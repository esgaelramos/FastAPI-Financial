"""Main module for the FastAPI-Financial application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import AppConfig
from .core.database import Database
from .api.v1.routes import router as v1_router


# Load the application configuration
app_config = AppConfig().config

# Create the database engine connection
database = Database(app_config['DATABASE_URL'])

# Init the FastAPI application
app = FastAPI()

# Configure the application for FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=app_config['DOMAIN'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(v1_router, prefix="/v1")
