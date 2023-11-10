from app import app
from flask_sqlalchemy import SQLAlchemy
from app.db import db

db = db.DatabaseManager()

class LocationTable(db.Model):
    """
    Represents the 'location_table' within the 'weatherwise' schema.

    Attributes:
    - location_id: Primary key for the table.
    - location_name: String field representing the name of the location.
    """
    __tablename__ = 'location_table'
    __table_args__ = {'schema': 'weatherwise'}  # Set the default schema here

    # Define the LocationTable class that represents the database table
    location_id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(20))

    def __init__(self):
        # Constructor for creating a new LocationTable instance
        pass
