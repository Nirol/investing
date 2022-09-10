"""Extensions module. Each extension is initialized in the investing_flask factory located in investing_flask.py."""
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
migrate = Migrate()
