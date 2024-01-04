"""Main module for the FastAPI-Financial application."""

import logging

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from .core.config import Settings
from .core.database import init_db
from .api.v1.routes import router as v1_router
from .schemas.responses_schema import ErrorResponse


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Load and Instance the Wrapper Settings
settings = Settings()

# Initialize the database
init_db()


# Init the FastAPI application
app = FastAPI()

# Configure the application for FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.DOMAIN,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the API routers (for versions)
app.include_router(v1_router, prefix="/v1")


# Handle Exceptions with custom Response
@app.exception_handler(HTTPException)
async def exception_handler(request, exc):
    """Handle Exceptions with custom Response."""
    logging.error(exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            success=False,
            message=exc.detail,
        ).model_dump()
    )
