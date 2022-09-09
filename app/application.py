"""The app module, containing the app factory function."""
import logging
import sys
from flask import Flask


from app.extensions import db, migrate


def create_app(config_object="app.settings"):
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.
    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    configure_logger(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)
    migrate.init_app(app, db)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""

    return None



def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)