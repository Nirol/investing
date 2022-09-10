"""The app module, containing the app factory function."""
import logging
import sys
from flask import Flask


from app.extensions import db, migrate

# import all models so flask db migration will recognize the models.



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
    from app.views import ad_units_bp
    app.register_blueprint(ad_units_bp)

    from app.views import line_item_bp
    app.register_blueprint(line_item_bp)

    from app.views import creative_bp
    app.register_blueprint(creative_bp)

    from app.views import fetch_bp
    app.register_blueprint(fetch_bp)

    return None



def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)
