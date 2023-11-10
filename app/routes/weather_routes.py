from flask import request, jsonify
from app import app
from app.controllers.sensor_controller import retrieve_metric, persist_metrics
from app.controllers.cache_controller import periodic_task, MetricCache, SensorCache
from app.middleware.requestFormatter import MetricsReportRequestSchema
from datetime import datetime
import threading
import json

# Create a thread for the periodic task
periodic_thread = threading.Thread(target=periodic_task, daemon=True)
# Start the thread
periodic_thread.start()

# You can access the in-memory data from the singleton as needed
metric_cache = MetricCache()
sensor_cache = SensorCache()


@app.route('/weather/report/<int:sensor_id>', methods=['POST'])
def report_metric(sensor_id):
    """
    API endpoint for reporting metrics from a sensor.

    - Validates the sensor ID.
    - Loads and validates incoming data using a schema.
    - Checks for missing metrics and persists data if validation passes.

    Returns JSON responses for success or failure.
    """

    # Validation: Check if sensor_id exists or not
    if sensor_id not in sensor_cache.data:
        return jsonify({'message': 'Sensor does not exists'})

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid data format"}), 400
    
    # Load and validate the data using the schema
    try:
        metrics_request_schema = MetricsReportRequestSchema()
        report_data = metrics_request_schema.load(data)
        print("Validation successful!")
    except Exception as e:
        print("Validation error:", str(e))
        return jsonify({'message': 'Invalid request body'})   

    # Check if all required metrics are present
    if not all(metric in data["metrics"] for metric in metric_cache.data.keys()):
        missing_metrics = [metric for metric in metric_cache.data.keys() if metric not in data["metrics"]]
        missing_metrics_message = f"Missing metrics: {', '.join(missing_metrics)}"
        print(missing_metrics_message)
        return jsonify({'message': missing_metrics_message}), 400
    
    # TO-DO
    # Some validation for the data based on sensor type
    # For e.g., For temperature - F or C - And validate its range
    try:
        persist_metrics(sensor_id=sensor_id, report_data=report_data)
        return jsonify({'message': "Metrics persisted sucessfully!"}), 201
    except Exception as e:
        # Here, error can be logged and responded with more specific error
        print("Exception: ", str(e))
        return jsonify({'Error': "Failed to persist metrics"}), 500  # Respond with an error message and a 500 status code

@app.route('/metrics/', methods=['GET'])
def get_metrics():
    """
    API endpoint to retrieve aggregated metrics.

    - Accepts sensor names, metrics, aggregation, start and end date as query parameters.
    - Performs validations for query parameters.
    - Retrieves and formats the metrics based on the query.
    - Returns aggregated metrics data in JSON format.
    """
    # Get sensor names from the query parameters
    sensor_ids = request.args.get('sensor', '').split(',')
    metric_ids = request.args.get('metrics', '').split(',')
    aggregation = request.args.get('aggregation', '')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # TO-DO: Validation can be done on all params
    # Convert empty strings to None for sensor_ids and metric_ids
    sensor_ids = sensor_ids if sensor_ids != [''] else None
    metric_ids = metric_ids if metric_ids != [''] else None

    # Convert empty strings to None
    start_date = start_date if start_date else None
    end_date = end_date if end_date else None


    # Validate date formats
    if start_date is not None and not is_valid_date(start_date):
        return jsonify({"error": "Invalid start_date format"}), 400
    if end_date is not None and not is_valid_date(end_date):

        return jsonify({"error": "Invalid end_date format"}), 400
    
    # TO-DO: Validation for the start_date should be before end_date

    # Check if aggregation is not provided or not in a predefined list
    valid_aggregations = ['avg', 'max', 'min', 'sum']  # TO-DO: This can be something configurable
    if aggregation not in valid_aggregations:
        return jsonify({"error": "Invalid aggregation requested"}), 400

    try:
        metrics = retrieve_metric(sensor_ids=sensor_ids, metric_ids=metric_ids, aggregation=aggregation, start_date=start_date, end_date=end_date)
        # Parse each string into a dictionary
        parsed_data = [json.loads(data_str) for data_str in metrics]
        # Return the metrics as JSON
        return jsonify(parsed_data), 200
    except Exception as e:
        # Here, error can be logged and responded with more specific error
        print("Exception: ", str(e))
        return jsonify({'Error': "Failed to persist metrics"}), 500  # Respond with an error message and a 500 status code


# TO-DO: Move it to the utility functions file
def is_valid_date(date_string):
    try:
        # Parse the date string
        datetime_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
        return True
    except ValueError:
        # If parsing fails, return False
        return False