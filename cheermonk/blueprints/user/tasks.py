from flask_babel import lazy_gettext as _

from cheermonk.blueprints.user.models import Business
from cheermonk.lib.flask_mailplus import send_template_message
from cheermonk.app import create_celery_app

celery = create_celery_app()


@celery.task()
def deliver_password_reset_email(cls, user_id, reset_token):
    """
    Send a reset password e-mail to a user.

    :param user_id: The user id
    :type user_id: int
    :param reset_token: The reset token
    :type reset_token: str
    :return: None if a user was not found
    """
    user = cls.query.get(user_id)

    if user is None:
        return

    ctx = {'user': user, 'reset_token': reset_token}

    send_template_message(subject=_('Password reset from Cheermonk'),
                          recipients=[user.email],
                          template='user/mail/password_reset', ctx=ctx)

    return None


@celery.task()
def delete_businesses(ids):
    """
    Delete businesses.

    :param ids: List of ids to be deleted
    :type ids: list
    :return: int
    """
    return Business.bulk_delete(ids)
