"""Test for Models of the User in the DataBase."""

from src.models.user import User


def test_user_model_attributes():
    """Test the attributes of the User model."""
    user_attrs = User.__table__.columns.keys()
    assert 'id' in user_attrs
    assert 'username' in user_attrs
    assert 'email' in user_attrs
    assert 'hashed_password' in user_attrs


def test_user_model_initialization():
    """Test initialization of User model."""
    user = User(
        username='testuser',
        email='test@example.com',
        hashed_password='hashed_pw'
    )

    assert user.username == 'testuser'
    assert user.email == 'test@example.com'
    assert user.hashed_password == 'hashed_pw'


def test_user_model_id_autoincrement():
    """Test if 'id' is set as autoincrement primary key."""
    id_column = User.__table__.columns['id']
    assert id_column.primary_key
    assert id_column.autoincrement


def test_user_model_username_unique():
    """Test if 'username' is set as unique."""
    username_column = User.__table__.columns['username']
    assert username_column.unique


def test_user_model_email_unique():
    """Test if 'email' is set as unique."""
    email_column = User.__table__.columns['email']
    assert email_column.unique
