"""
sql_queries lists the path of the jinja templated SQL
queries to create/update tables
"""

SCHEMA_CREATE = "app/scripts/templates/0_create_schema.jinja2"
INSERT_DUMMY_DATA = "app/scripts/templates/5_insert_dummy_data.jinja2"

CREATE_TABLE_QUERIES = {
    "metrics_table": "app/scripts/templates/1_create_metrics_table.jinja2",
    "location_table": "app/scripts/templates/2_create_location_table.jinja2",
    "sensors_table": "app/scripts/templates/3_create_sensor_table.jinja2",
    "reports_table": "app/scripts/templates/4_create_reports_table.jinja2",
}
