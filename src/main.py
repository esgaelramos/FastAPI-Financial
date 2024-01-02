"""Main module for the FastAPI-Financial application."""

import logging

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from .core.config import AppConfig
from .core.database import Database
from .api.v1.routes import router as v1_router
from .schemas.responses_schema import ErrorResponse


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Load the application configuration
app_config = AppConfig().config

# Create the database engine connection
try:
    database = Database(app_config['DATABASE_URL'])
    logging.info('Database connection established.')
except Exception:  # pragma: no cover
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


# Handle Exceptions with custom Response
@app.exception_handler(HTTPException)
async def exception_handler(request, exc):
    """Handle Exceptions with custom Response."""
    logging.error(exc.detail)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            success=False,
            message=exc.detail,
        ).model_dump()
    )
