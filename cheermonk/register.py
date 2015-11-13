from flask import render_template

from cheermonk.extensions import db, bcrypt, login_manager, webpack
from cheermonk.blueprints.page import page
from cheermonk.blueprints.user import user

from jinja2 import ChoiceLoader, FileSystemLoader

FLASK_BLUEPRINTS = [page, user]

CUSTOM_ERROR_PAGES = [404, 500, 502]


def blueprints(app):
    for blueprint in FLASK_BLUEPRINTS:
        app.register_blueprint(blueprint)

    return None


def extensions(app):
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    webpack.init_app(app)


def template_processors(app):
    """
    Register 0 or more custom template processors (mutates the app passed in).

    :param app: Flask application instance
    :return: App jinja environment
    """
    public_build_path = app.config.get('PUBLIC_BUILD_PATH')

    if public_build_path:
        multiple_template_loader = ChoiceLoader([
            app.jinja_loader,
            FileSystemLoader([public_build_path]),
        ])
        app.jinja_loader = multiple_template_loader

    app.jinja_env.add_extension('jinja2.ext.do')

    return app.jinja_env


def error_templates(app):
    """
    Register 0 or more error handlers (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """

    def render_status(status):
        """
         Render a custom template for a specific status.
           Source: http://stackoverflow.com/a/30108946

         :param status: Status as a written name
         :type status: str
         :return: None
         """
        # Get the status code from the status, default to a 500 so that we
        # catch all types of errors and treat them as a 500.
        status_code = getattr(status, 'code', 500)
        return render_template('{0}.html'.format(status_code)), status_code

    for error in CUSTOM_ERROR_PAGES:
        app.errorhandler(error)(render_status)

    return None
