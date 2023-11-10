from flask_sqlalchemy import SQLAlchemy
from app import app

class DatabaseManager:
    """
        Returns the SQLAlchemy instance as a singleton when creating the DatabaseManager object.

        The __new__ method ensures only a single instance of the SQLAlchemy object is created and shared across the app.

        Returns:
        The SQLAlchemy instance used by the Flask application.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = SQLAlchemy(app)
        return cls._instance

# Usage: You can use the DatabaseManager class to get the SQLAlchemy instance in your Flask app.
# For example, in your app/__init__.py:
# db = DatabaseManager()
# Singleton class will make sure only single instance is used across the application
