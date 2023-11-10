from app.models.reports_model import ReportsTable
from app.controllers.cache_controller import MetricCache, SensorCache
from app.db import db
from datetime import datetime
from flask import current_app
from sqlalchemy import cast, TIMESTAMP,  and_, or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text, func, exists
import pandas as pd

# Initialize the DatabaseManager instance
db = db.DatabaseManager()

# Create instances of MetricCache and SensorCache
metric_cache = MetricCache()
sensor_cache = SensorCache()

def execute_db_query(query):
    """
    Executes a database query using the provided query object and returns the result in a DataFrame.
    """
    result = pd.read_sql(query.statement, current_app.config['DB_ENGINE'])
    return result


def persist_metrics(sensor_id, report_data):
    """
    Persists metrics data into the database.

    Arguments:
    - sensor_id: ID of the sensor sending the report.
    - report_data: Dictionary containing reported metrics and their values.
    """
    try:
        # Iterate over each metric and create a record
        casted_recorded_at = cast(report_data["recorded_at"], TIMESTAMP)
        for metric, value in report_data["metrics"].items():
            record = ReportsTable(
                sensor_id=sensor_id,
                metric_id=metric_cache.data[metric],  #  metric_cache contains metric_id mappings
                metric_val=value,
                recorded_at=casted_recorded_at,
                created_at=datetime.utcnow()
            )
            # Add the record to the session
            db.session.add(record)

        # Commit the changes to the database
        db.session.commit()
        db.session.close()

    except SQLAlchemyError as e:
        # If there's a database error, you can log the error and raise a custom exception
        print(f"Database error: {str(e)}")
        raise e

    except Exception as e:
        # Handle any other unexpected errors and raise a custom exception
        print(f"Unexpected error: {str(e)}")
        raise e

def fetch_metric_data(sensor_id, metric_ids, aggregation, start_date, end_date):
    """
    Fetches metric data based on provided parameters.

    Arguments:
    - sensor_id: ID of the sensor.
    - metric_ids: List of metric IDs to fetch data for.
    - aggregation: Type of aggregation function ('avg', 'max', 'min', 'sum').
    - start_date: Start date for the data retrieval period.
    - end_date: End date for the data retrieval period.
    """
    # Mapping of aggregation functions to SQLAlchemy functions
    aggregation_functions = {
        'avg': func.avg,
        'max': func.max,
        'min': func.min,
        'sum': func.sum,
    }

    # Set the default aggregation function to func.avg if aggregation is not specified or not in the mapping
    selected_aggregation = aggregation_functions.get(aggregation, func.avg)

    try:

        if start_date is not None:
                if end_date is None:
                    end_date = datetime.utcnow()
                start_date = cast(start_date, TIMESTAMP)
                end_date = cast(end_date, TIMESTAMP)
                query = current_app.config['DB_SESSION'].query(
                ReportsTable.sensor_id,
                ReportsTable.metric_id,
                selected_aggregation(ReportsTable.metric_val)). \
                filter(
                    and_(
                        ReportsTable.sensor_id == sensor_id,
                        ReportsTable.metric_id.in_(metric_ids),
                        ReportsTable.recorded_at.between(start_date, end_date)
                    )
                ).group_by(
                    ReportsTable.sensor_id,
                    ReportsTable.metric_id,
                )
        else:
            query = current_app.config['DB_SESSION'].query(
                ReportsTable.sensor_id,
                ReportsTable.metric_id,
                selected_aggregation(ReportsTable.metric_val)). \
                filter(
                    and_(
                        ReportsTable.sensor_id == sensor_id,
                        ReportsTable.metric_id.in_(metric_ids),
                    )
                ).group_by(
                    ReportsTable.sensor_id,
                    ReportsTable.metric_id,
                )
        
        # Execute the query against DB
        df = execute_db_query(query)
        
    except SQLAlchemyError as e:
        # If there's a database error, you can log the error and raise a custom exception
        print(f"Database error: {str(e)}")
        raise e

    except Exception as e:
        # Handle any other unexpected errors and raise a custom exception
        print(f"Unexpected error: {str(e)}")
        raise e

    # Pivot the DataFrame
    agg_val = aggregation + "_1" # TO-DO: Optimize it
    df = df.pivot(index='sensor_id', columns='metric_id', values=agg_val).reset_index()
    df = df.rename_axis(columns=None)

    # metric_cache.data is mapping dictionary for column renaming
    # Identify columns to rename based on the mapping dictionary
    columns_to_rename = {matric_id: f"{matric_name}" for matric_name, matric_id in metric_cache.data.items() if matric_id in df.columns}

    # Rename the identified columns
    df = df.rename(columns=columns_to_rename)

    if not df.empty:
        json_data = df.to_json(orient='records')
        return json_data
    else:
        return None # Dataframe is empty
   

def retrieve_metric(sensor_ids=None, metric_ids=None, aggregation=None, start_date=None, end_date=None):
    """
    Retrieves metrics based on the provided parameters.

    Arguments:
    - sensor_ids: List of sensor IDs to retrieve data from. If None, retrieves from all sensors.
    - metric_ids: List of metric IDs to retrieve. If None, retrieves all available metrics.
    - aggregation: Type of aggregation function ('avg', 'max', 'min', 'sum').
    - start_date: Start date for the data retrieval period.
    - end_date: End date for the data retrieval period.

    Returns:
    A list containing JSON data of retrieved metrics based on the provided parameters.
    """
    # If metric id is none than pass all else pass specific
    if metric_ids is None:
        metric_ids = metric_cache.data.values()

    # If sensor_ids is none than pass all else pass specific
    if sensor_ids is None:
        sensor_ids = list(sensor_cache.data)

    response = []
    for sensor_id in sensor_ids:
        data = fetch_metric_data(sensor_id, metric_ids, aggregation, start_date, end_date)
        if data is not None:
            response.append(data)

    return response

# Following function is not required and not needed to query db for serving each request
# instead we store sensor_ids and metric_ids into memory

# def is_sensor_id_exists(sensor_id):
#     # Create a query that checks if the given sensor_id exists in the SensorTable
#     query = current_app.config['DB_SESSION'].query(exists().where(SensorTable.sensor_id == sensor_id))
#     # Execute the query and return the result (True if exists, False otherwise)
#     return db.session.scalar(query)


# Following function used to test DB connection
# TO-DO: On application start check DB connection with this function

# def test_connnection():
#     try:
#         db.session.query(text('1')).from_statement(text('SELECT 1')).all()
#         print("It works!")
#     except Exception as e:
#         # e holds description of the error
#         print("Broke", e)
    