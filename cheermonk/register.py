from cheermonk.blueprints.page import page

FLASK_BLUEPRINTS = [page]


def blueprints(app):
    for blueprint in FLASK_BLUEPRINTS:
        app.register_blueprint(blueprint)

    return None
