"""Main module for the FastAPI-Financial application."""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import AppConfig
from .core.database import Database
from .api.v1.routes import router as v1_router


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Load the application configuration
app_config = AppConfig().config

# Create the database engine connection
try:  # pragma: no cover
    database = Database(app_config['DATABASE_URsL'])
    logging.info('Database connection established.')
except KeyError:
    database = Database('sqlite:///:memory:')
    logging.warning('Database connection failed. Using in-memory database.')

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
