"""Module `database` for setup the connection."""

import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from src.core.config import Settings


# Instance the Wrapper Settings
settings = Settings()


def create_engine_with_fallback(database_url: str):
    """Create the database engine or fallback to SQLite."""
    try:
        logging.info(f"Connecting to the database {database_url}")
        return create_engine(database_url)
    except Exception as e:  # pragma: no cover
        logging.warning(f"Database connection FAIL: {e}. Using db in-memory.")
        return create_engine('sqlite:///:memory:')


# Create the database engine or fallback to SQLite
engine = create_engine_with_fallback(settings.DATABASE_URL)
default_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)


def get_session():
    """Provide a transactional scope around a series of operations."""
    db_session = default_session()
    try:
        yield db_session
    finally:
        db_session.close()


def init_db():
    """Initialize the database and create all tables."""
    Base.metadata.create_all(bind=engine)


# Instance the Base for use in the Models
Base = declarative_base()
