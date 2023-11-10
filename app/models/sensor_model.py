from app import app
from flask_sqlalchemy import SQLAlchemy
from app.db import db

db = db.DatabaseManager()

class SensorTable(db.Model):
    """
    Represents the 'reports_table' within the 'weatherwise' schema.

    Attributes:
    - report_id: Primary key for the table.
    - sensor_id: Integer field for the sensor ID.
    - metric_id: Integer field for the metric ID.
    - metric_val: String field representing the value of the metric.
    - recorded_at: Datetime field for the recorded time.
    - created_at: Datetime field for the creation time of the record.
    """
    __tablename__ = 'sensor_table'
    __table_args__ = {'schema': 'weatherwise'}  # Set the default schema here

    # Define the SensorTable class that represents the database table
    sensor_id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer)

    def __init__(self):
        # Constructor for creating a new SensorTable instance
        pass
