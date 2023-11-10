from app import app
from flask_sqlalchemy import SQLAlchemy
from app.db import db
db = db.DatabaseManager()

class ReportsTable(db.Model):
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
    __tablename__ = 'reports_table'
    __table_args__ = {'schema': 'weatherwise'}  # Set the default schema here

    # Define the ReportsTable class that represents the database table
    report_id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer)
    metric_id = db.Column(db.Integer)
    metric_val = db.Column(db.String(20))
    recorded_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime)

    def __init__(self, sensor_id, metric_id, metric_val, recorded_at, created_at):
        # Constructor for creating a new ReportsTable instance
        self.sensor_id = sensor_id
        self.metric_id = metric_id
        self.metric_val = metric_val
        self.recorded_at = recorded_at
        self.created_at = created_at
