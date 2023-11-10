from datetime import datetime, timedelta
from faker import Faker
import random

# Define the number of metrics, sensors, locations, and reports
NO_OF_METRICS=3
NO_OF_SENSOR=10
NO_OF_LOCATIONS=30
NO_OF_REPORTS=10

fake = Faker() # Initialize a Faker instance for generating fake data

def generate_ids(nums_records: int):
    # Generate a list of incremental IDs
    return [i for i in range(1, nums_records+1)]

def generate_location_data(ids):
    # Generate location data with corresponding IDs and random location names
    data = []
    for id in ids:
        data.append({
            'location_id': id,
            'location_name': fake.city()
        })
    return data

def generate_sensor_data(ids, location_ids):
     # Generate sensor data with corresponding IDs and random location IDs
    data = []
    for id in ids:
        data.append({
            'sensor_id': id,
            'location_id': random.choice(location_ids)
        })
    return data

def generate_report_data(ids, sensor_ids, metric_ids, days):
    # Generate report data using provided IDs, metrics, sensors, and specified days range
    start_date = datetime.now() - timedelta(days=days)
    time_between_records = timedelta(days=days / len(ids))
    data = []

    for id in range(1, len(ids)+1):
        for each_metric in metric_ids:
            data.append({
                'report_id': id,
                'sensor_id': random.choice(sensor_ids),
                'metric_id': each_metric,
                'metric_val': random.randint(0, 100),
                'recorded_at': start_date + id * time_between_records,
                'created_at': start_date + id * time_between_records
            })

    return data

def generate_data():
    # Generate all required data: metrics, sensor, location, and reports
    metric_data = [
        {'metric_id': 1, 'metric_name': 'Temperature'},
        {'metric_id': 2, 'metric_name': 'Humidity'},
        {'metric_id': 3, 'metric_name': 'Wind_Speed'}
    ]

    metric_ids = generate_ids(NO_OF_METRICS)
    sensor_ids = generate_ids(NO_OF_SENSOR)
    location_ids = generate_ids(NO_OF_LOCATIONS)
    reports_ids = generate_ids(NO_OF_REPORTS)

    sensor_data = generate_sensor_data(sensor_ids, location_ids)
    location_data = generate_location_data(location_ids)
    report_data = generate_report_data(reports_ids, sensor_ids, metric_ids, 7)


    return metric_data, sensor_data, location_data, report_data