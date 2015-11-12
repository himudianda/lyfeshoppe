from cheermonk.extensions import db, webpack
from cheermonk.blueprints.page import page

FLASK_BLUEPRINTS = [page]


def blueprints(app):
    for blueprint in FLASK_BLUEPRINTS:
        app.register_blueprint(blueprint)

    return None


def extensions(app):
    db.init_app(app)
    webpack.init_app(app)
