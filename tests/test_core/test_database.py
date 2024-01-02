"""Tests for the DataBase Module."""

import unittest
from unittest.mock import MagicMock, patch

from src.core.database import create_engine_with_fallback, get_session


class TestDatabase(unittest.TestCase):
    """Test the Database class."""

    @patch('src.core.database.create_engine')
    @patch('src.core.database.sessionmaker')
    def setUp(self, mock_sessionmaker, mock_create_engine):
        """Set up the test case."""
        self.database_url = 'sqlite:///:memory:'
        self.mock_engine = mock_create_engine.return_value
        self.mock_sessionmaker = mock_sessionmaker
        self.db = create_engine_with_fallback(self.database_url)

    @patch('src.core.database.create_engine')
    def test_create_engine_with_fallback(self, mock_create_engine):
        """Test create_engine_with_fallback function."""
        # Simula la creación exitosa del motor de la base de datos
        mock_create_engine.return_value = MagicMock()

        # Llama a la función con un URL de base de datos
        engine = create_engine_with_fallback(self.database_url)

        # Verifica que create_engine fue llamado con el URL correcto
        mock_create_engine.assert_called_once_with(self.database_url)
        self.assertIsNotNone(engine)

    @patch('src.core.database.default_session')
    def test_get_session(self, mock_default_session):
        """Test the get_session method."""
        mock_session = MagicMock()
        mock_default_session.return_value = mock_session

        # Obtén el generador de sesión
        session_gen = get_session()

        # Emula el comportamiento de entrar y salir del contexto
        session = next(session_gen)
        self.assertEqual(session, mock_session)

        try:
            next(session_gen)
        except StopIteration:
            pass

        # Verifica que la sesión se cerró correctamente
        mock_session.close.assert_called_once()
