from app import app
from flask_sqlalchemy import SQLAlchemy
from app.db import db

db = db.DatabaseManager()

class SensorTable(db.Model):
    """
    Represents the 'sensors_table' within the 'weatherwise' schema.

    Attributes:
    - sensor_id: Integer field for the sensor ID.
    - location_id: Foreign key for the location table.
    """
    __tablename__ = 'sensors_table'
    __table_args__ = {'schema': 'weatherwise'}  # Set the default schema here

    # Define the SensorTable class that represents the database table
    sensor_id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer)

    def __init__(self):
        # Constructor for creating a new SensorTable instance
        pass
