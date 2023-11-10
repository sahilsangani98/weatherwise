import psycopg2
import sql_queries
from psycopg2 import sql
from jinja2 import Template
from data_generation import generate_data

# Generate data for metrics, sensors, locations, and reports
metric_data, sensor_data, location_data, report_data = generate_data()

# Configure based on requirement and your setup
DB_NAME = "weatherdb"
DB_USER = "postgres"
DB_PASSWORD = "1234"
DB_HOST = "localhost"

# Context with variables for the template
CONTEXT = {
    'schema_name': 'weatherwise',
    'not_exists' : True, # Controls table existence checks
    'sensor_data': sensor_data,
    'metric_data': metric_data,
    'report_data': report_data,
    'location_data': location_data,
}

def execute_jinja_template_query(template_path, context, db_connection):
    # Execute SQL queries defined in Jinja template
    with open(template_path, 'r') as file:
        template_str = file.read()
        template = Template(template_str)
        query = template.render(context)

        cursor = db_connection.cursor()

        try:
            cursor.execute(query)
            db_connection.commit()
        except psycopg2.Error as e:
            print("Error executing the query:", str(e))
            db_connection.rollback()

        cursor.close()


def create_schema(db_handle, query):
    """
    Create the schema based on the passed in parameter
    """
    execute_jinja_template_query(query, CONTEXT, db_handle)
    print("Schema: {0} created if not exist".format(CONTEXT['schema_name']))

def create_tables(db_handle, queries):
    """
    Create the tables based on the passed in parameter
    """
    for table_name, template_path in queries.items():
        CONTEXT['table_name'] = table_name
        execute_jinja_template_query(template_path, CONTEXT, db_handle)
        print("{0} created if not exist".format(table_name))

def insert_dummy_data(db_handle, query):
    # Insert dummy data into the schema
    execute_jinja_template_query(query, CONTEXT, db_handle)
    print("Dummy data inserted for schema: {0}".format(CONTEXT['schema_name']))


def connect_to_postgres(dbname, user, password, host):
    # Establish a connection to the Postgres database
    return psycopg2.connect(dbname=dbname, user=user, password=password, host=host)


def main():
    """
    Main program to create the inital tables for NWDAF in vertica
    """
    try:
        db_handle = connect_to_postgres(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST)

        create_schema(db_handle, sql_queries.SCHEMA_CREATE)
        create_tables(db_handle, sql_queries.CREATE_TABLE_QUERIES)
        insert_dummy_data(db_handle, sql_queries.INSERT_DUMMY_DATA)

    except Exception as e:
        raise Exception("Query Failed:\n", str(e))

if __name__ == "__main__":
    main()