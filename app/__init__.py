from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(
    os.getenv('POSTGRES_USER', 'postgres'),
    os.getenv('POSTGRES_PASSWORD', '1234'),
    os.getenv('POSTGRES_HOST', '127.0.0.1'),
    os.getenv('POSTGRES_PORT', '5432'),
    os.getenv('POSTGRES_DB', 'weatherdb')
    )

app.config.from_object("app.configuration.config.Config")

from app.routes import weather_routes
