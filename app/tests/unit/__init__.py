# app/tests/__init__.py

import unittest
from flask_testing import TestCase
from flask import Flask
from app.db import db
from app import app as a
import os

class BaseTestCase(TestCase):
    """Base test case for the Flask application."""

    def create_app(self):
        """Create and configure the Flask app for testing."""

        app = Flask(__name__)
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        from app.routes import weather_routes
        app.config['TESTING'] = True
        return app

if __name__ == '__main__':
    unittest.main()
