from flask_babel import lazy_gettext as _

from lyfeshoppe.lib.flask_mailplus import send_template_message
from lyfeshoppe.app import create_celery_app
from lyfeshoppe.blueprints.user.models import User
from lyfeshoppe.blueprints.business.models.business import Business, Customer

celery = create_celery_app()


@celery.task()
def request_customer_review(business_id, customer_id):
    """
    Send a customer review request for business

    :param user_id: The user id
    :type user_id: int
    :param reset_token: The reset token
    :type reset_token: str
    :return: None if a user was not found
    """
    business = Business.query.get(business_id)
    customer = Customer.query.get(customer_id)
    user = User.query.get(customer.user.id)

    if business is None or user is None:
        return

    ctx = {'user': user, 'business': business}

    send_template_message(subject=_('Review request from ' + business.name),
                          recipients=[user.email],
                          template='mail/business/review_request', ctx=ctx)

    return None
