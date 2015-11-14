from flask import Flask
from celery import Celery

from cheermonk.blueprints.user.models import User
from cheermonk.register import blueprints, extensions, template_processors, error_templates
from cheermonk.initialize import authentication


CELERY_TASK_LIST = [
    'cheermonk.blueprints.user.tasks'
]


def create_celery_app(app=None):
    """
    Create a new celery object and tie together the celery config to the app's
    config. Wrap all tasks in the context of the application.

    :param app: Flask app
    :return: Celery app
    """
    app = app or create_app()

    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'],
                    include=CELERY_TASK_LIST)
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


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
