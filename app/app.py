from flask import Flask
from app import auth
from app.extensions import db, migrate


def create_app(config_object='app.settings'):
    """Create App

    :config_class: App Config Class
    :returns: app context

    """
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)
    migrate.init_app(app, db)
    return None


def register_blueprints(app):
    """Register FLask blueprints."""
    app.register_blueprint(auth.views.bp)
    return None
