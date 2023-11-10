import threading
import time
from app import app  # Assuming you have the Flask app instance
from app.db import db
from flask import current_app
from app.models.metrics_model import MetricsTable
from app.models.sensor_model import SensorTable

db = db.DatabaseManager()

class MetricCache:
    """
    Singleton class to store metric information in memory.
    """
    # Sample in-memory values: {'temperature': 1, 'humidity': 2, 'wind_speed': 3}
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        """
        Ensure only one instance of MetricCache exists.
        """
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.data = None
            return cls._instance

class SensorCache:
    """
    Singleton class to store sensor information in memory.
    """
    # Sample in-memory sensor_id values: {1, 2, 3, 4}
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        """
        Ensure only one instance of SensorCache exists.
        """
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.data = None
            return cls._instance

def fetch_and_update_metrics():
    """
    Fetches and updates metrics information in the in-memory cache.
    """
    # Create an application context
    with app.app_context():
        # Fetch metric_id and metric_name from the database
        query = current_app.config['DB_SESSION'].query(
            MetricsTable.metric_id,
            MetricsTable.metric_name
            )

        # Fetch the results
        results = query.all()
    
    # Create a dictionary with the names as keys
    result_dict = {name.lower(): identifier for identifier, name in results}

    metric_cache = MetricCache()
    metric_cache.data = result_dict


def fetch_and_update_sensors():
    """
    Fetches and updates sesnsors information in the in-memory cache.
    """
    # Create an application context
    with app.app_context():
        # Fetch metric_id and metric_name from the database
        query = current_app.config['DB_SESSION'].query(
            SensorTable.sensor_id
            )

        # Fetch the results
        results = query.all()
    
    # Create a set with the sensor_id
    # Convert the list of tuples into a set
    result_set = {item[0] for item in results}

    sensor_cache = SensorCache()
    sensor_cache.data = result_set


def periodic_task():
    """
    Runs tasks to periodically fetch and update metric and sensor data in the in-memory cache.
    """
    while True:
        # Run the fetch_and_update_metrics function
        fetch_and_update_metrics()
        fetch_and_update_sensors()
        print("In-memory Sensors Cache: ", SensorCache()._instance.data)
        print("In-memory Metric Cache: ", MetricCache()._instance.data.keys())

        # Sleep for 5 minutes before the next execution
        time.sleep(300)  # TO-DO: Make it configurable