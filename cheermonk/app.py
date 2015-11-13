from flask import Flask

from cheermonk.blueprints.user.models import User
from cheermonk.register import blueprints, extensions, template_processors, error_templates
from cheermonk.initialize import authentication


def create_app():
    app = Flask(__name__)
    configure_settings(app)

    # Register
    blueprints(app)
    extensions(app)
    template_processors(app)
    error_templates(app)

    # Initialize.
    authentication(app, User)

    return app


def configure_settings(app):
    """
    Modify the settings of the application (mutates the app passed in).
    """
    app.config.from_object('config.settings')

    return app.config
