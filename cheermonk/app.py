from flask import Flask

from cheermonk.register import blueprints


def create_app():
    app = Flask(__name__)

    # Register
    blueprints(app)

    return app
