from flask_babel import lazy_gettext as _

from lyfeshoppe.lib.flask_mailplus import send_template_message
from lyfeshoppe.app import create_celery_app
from lyfeshoppe.blueprints.user.models import User

celery = create_celery_app()


@celery.task()
def deliver_password_reset_email(user_id, reset_token):
    """
    Send a reset password e-mail to a user.

    :param user_id: The user id
    :type user_id: int
    :param reset_token: The reset token
    :type reset_token: str
    :return: None if a user was not found
    """
    user = User.query.get(user_id)

    if user is None:
        return

    ctx = {'user': user, 'reset_token': reset_token}

    send_template_message(subject=_('Password reset from LyfeShoppe'),
                          recipients=[user.email],
                          template='mail/user/password_reset', ctx=ctx)

    return None


@celery.task()
def deliver_referral_email(ref_user_id, sender_id, reset_token):
    """
    Send a reset password e-mail to a user.

    :param user_id: The user id
    :type user_id: int
    :param reset_token: The reset token
    :type reset_token: str
    :return: None if a user was not found
    """
    ref_user = User.query.get(ref_user_id)
    sender = User.query.get(sender_id)

    if not ref_user or not sender:
        return

    ctx = {'sender': sender, 'ref_user': ref_user, 'reset_token': reset_token}

    send_template_message(subject=_("Invitation from " + sender.name),
                          recipients=[sender.email, ref_user.email],
                          template='mail/user/referral_sent', ctx=ctx)

    return None
