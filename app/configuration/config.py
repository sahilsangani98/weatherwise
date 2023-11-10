import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

class Config():
    """ Configuration class for the WeatherWise application settings.

        DB_URL: The URL constructed using environment variables for Postgres connection.
    """
    DB_URL = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(
    os.getenv('POSTGRES_USER', 'postgres'),
    os.getenv('POSTGRES_PASSWORD', '1234'),
    os.getenv('POSTGRES_HOST', '127.0.0.1'),
    os.getenv('POSTGRES_PORT', '5432'),
    os.getenv('POSTGRES_DB', 'weatherdb')
    )

    # DB_ENGINE: The SQLAlchemy engine object initialized using the DB_URL.
    # It enables interaction with the database.
    DB_ENGINE = create_engine(DB_URL, echo=True)

    # DB_SESSION: The SQLAlchemy session object.
    # It's created using a sessionmaker bound to the DB_ENGINE.
    DB_SESSION = sessionmaker(bind=DB_ENGINE)()
    