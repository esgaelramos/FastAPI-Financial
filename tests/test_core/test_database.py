"""Tests for the DataBase Module."""

import unittest
from unittest.mock import (
    ANY, MagicMock, patch, call
)

from src.core.database import Database


class TestDatabase(unittest.TestCase):
    """Test the Database class."""

    @patch('src.core.database.create_engine')
    @patch('src.core.database.sessionmaker')
    def setUp(self, mock_sessionmaker, mock_create_engine):
        """Set up the test case."""
        self.database_url = 'sqlite:///:memory:'
        self.mock_engine = mock_create_engine.return_value
        self.mock_sessionmaker = mock_sessionmaker
        self.db = Database(self.database_url)

    def test_init(self):
        """Test initialization of Database class."""
        self.mock_sessionmaker.assert_called_with(
            autocommit=False, autoflush=False, bind=self.mock_engine
        )

    @patch('src.core.database.sessionmaker')
    def test_get_session(self, mock_sessionmaker):
        """Test the get_session method of Database class."""
        mock_session_class = MagicMock()
        mock_sessionmaker.return_value = mock_session_class
        mock_session = mock_session_class.return_value

        db = Database(self.database_url)

        with db.get_session() as session:
            self.assertEqual(session, mock_session)

        mock_session_class.assert_called_once()
        mock_session.close.assert_called_once()

    @patch('src.core.database.Database.get_session')
    def test_execute(self, mock_get_session):
        """Test execute method of Database class."""
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        query = "CREATE TABLE test_table (id INTEGER PRIMARY KEY)"
        self.db.execute(query)

        mock_session.assert_has_calls([
            call.execute(ANY),
            call.commit()
        ])
