from app import app
from flask_sqlalchemy import SQLAlchemy
from app.db import db

db = db.DatabaseManager()

class MetricsTable(db.Model):
    """
    Represents the 'metrics_table' within the 'weatherwise' schema.

    Attributes:
    - metric_id: Primary key for the table.
    - metric_name: String field representing the name of the metric.
    """
    __tablename__ = 'metrics_table'
    __table_args__ = {'schema': 'weatherwise'}  # Set the default schema here

    # Define the MetricsTable class that represents the database table
    metric_id = db.Column(db.Integer, primary_key=True)
    metric_name = db.Column(db.String(20))

    def __init__(self):
        # Constructor for creating a new MetricsTable instance
        pass
