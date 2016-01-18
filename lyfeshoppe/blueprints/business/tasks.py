from flask_babel import lazy_gettext as _

from lyfeshoppe.lib.flask_mailplus import send_template_message
from lyfeshoppe.app import create_celery_app
from lyfeshoppe.blueprints.user.models import User
from lyfeshoppe.blueprints.business.models.business import Business, Customer, Employee

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


@celery.task()
def notify_business_create(business_id, user_id):
    """
    Notify when the business is created

    :param user_id: The user id
    :type user_id: int
    :param reset_token: The reset token
    :type reset_token: str
    :return: None if a user was not found
    """
    business = Business.query.get(business_id)
    user = User.query.get(user_id)

    if not business or not user:
        return

    ctx = {'user': user, 'business': business}

    send_template_message(subject=_('Your business ' + business.name + ' has been created'),
                          recipients=[user.email, business.email],
                          template='mail/business/business_created', ctx=ctx)

    return None


@celery.task()
def notify_customer_create(business_id, customer_id, owner_id, reset_token):
    """
    Notify when the business is created

    :param user_id: The user id
    :type user_id: int
    :param reset_token: The reset token
    :type reset_token: str
    :return: None if a user was not found
    """
    business = Business.query.get(business_id)
    customer = User.query.get(customer_id)
    owner = User.query.get(owner_id)

    if not business or not customer or not owner:
        return

    ctx = {'customer': customer, 'business': business, 'owner': owner, 'reset_token': reset_token}

    send_template_message(subject=_('Customer at ' + business.name),
                          recipients=[owner.email, business.email, customer.email],
                          template='mail/customer/customer_created', ctx=ctx)

    return None


@celery.task()
def notify_employee_create(business_id, employee_id, owner_id, reset_token):
    """
    Notify when the business is created

    :param user_id: The user id
    :type user_id: int
    :param reset_token: The reset token
    :type reset_token: str
    :return: None if a user was not found
    """
    business = Business.query.get(business_id)
    employee = User.query.get(employee_id)
    owner = User.query.get(owner_id)

    if not business or not employee or not owner:
        return

    ctx = {'employee': employee, 'business': business, 'owner': owner, 'reset_token': reset_token}

    send_template_message(subject=_('Employee at ' + business.name),
                          recipients=[owner.email, business.email, employee.email],
                          template='mail/employee/employee_created', ctx=ctx)

    return None
