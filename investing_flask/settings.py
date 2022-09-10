# -*- coding: utf-8 -*-
"""Application configuration.

Most configuration is set via environment variables.

For local development, use a .env file to set
environment variables.
"""
from environs import Env

env = Env()
env.read_env()

database_uri = "postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}".format(
    dbuser=env.str("DBUSER"), dbpass=env.str("DBPASS"), dbhost=env.str("DBHOST"), dbname=env.str("DBNAME")
)

ENV = env.str("FLASK_ENV", default="production")
DEBUG = ENV == "development"
SQLALCHEMY_DATABASE_URI = database_uri
SQLALCHEMY_TRACK_MODIFICATIONS = False
