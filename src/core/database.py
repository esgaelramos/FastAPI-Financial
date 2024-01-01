"""Module `database` for setup the connection."""

from contextlib import contextmanager

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


class Database:
    """Class for the database connection."""

    def __init__(self, database_url: str):
        """Init the database connection."""
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    @contextmanager
    def get_session(self):
        """Get a session from the database."""
        db_session = self.SessionLocal()
        try:
            yield db_session
        finally:
            db_session.close()

    def execute(self, query: str):
        """Execute a query in the database."""
        with self.get_session() as session:
            session.execute(text(query))
            session.commit()
