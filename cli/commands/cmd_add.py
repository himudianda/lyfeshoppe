import logging
import random
from datetime import datetime
import click
from faker import Faker

from cheermonk.app import create_app
from cheermonk.extensions import db
from cheermonk.blueprints.issue.models import Issue
from cheermonk.blueprints.user.models import User
from cheermonk.blueprints.common.models import Address, Availability, Occupancy
from cheermonk.blueprints.billing.models.invoice import Invoice
from cheermonk.blueprints.billing.models.coupon import Coupon
from cheermonk.blueprints.billing.gateways.stripecom import Coupon as PaymentCoupon
from cheermonk.blueprints.business.models.business import Business, Employee

SEED_ADMIN_EMAIL = None
ACCEPT_LANGUAGES = None

try:
    from instance import settings

    SEED_ADMIN_EMAIL = settings.SEED_ADMIN_EMAIL
    ACCEPT_LANGUAGES = settings.ACCEPT_LANGUAGES
except ImportError:
    logging.error('Ensure __init__.py and settings.py both exist in instance/')
    exit(1)
except AttributeError:
    from config import settings

    if SEED_ADMIN_EMAIL is None:
        SEED_ADMIN_EMAIL = settings.SEED_ADMIN_EMAIL

    if ACCEPT_LANGUAGES is None:
        ACCEPT_LANGUAGES = settings.ACCEPT_LANGUAGES

fake = Faker()
app = create_app()
db.app = app

NUM_OF_FAKE_ADDRESSES = 25
NUM_OF_FAKE_USERS = 50
NUM_OF_FAKE_ISSUES = 50
NUM_OF_FAKE_COUPONS = 5
NUM_OF_FAKE_BUSINESSES = 200


def _log_status(count, model_label):
    """
    Log the output of how many records were created.

    :param count: Amount created
    :type count: int
    :param model_label: Name of the model
    :type model_label: str
    :return: None
    """
    click.echo('Created {0} {1}'.format(count, model_label))

    return None


def _bulk_insert(model, data, label):
    """
    Bulk insert data to a specific model and log it.

    :param model: Model being affected
    :type model: SQLAlchemy
    :param data: Data to be saved
    :type data: list
    :param label: Label for the output
    :type label: str
    :return: None
    """
    with app.app_context():
        model.query.delete()
        db.session.commit()
        db.engine.execute(model.__table__.insert(), data)

        _log_status(model.query.count(), label)

    return None


@click.group()
def cli():
    """ Populate your db with generated data. """
    pass


@click.command()
def addresses():
    """
        Create random addresses
    """
    data = []
    for i in range(0, NUM_OF_FAKE_ADDRESSES):
        params = {
            'street': fake.street_address(),
            'city': fake.city(),
            'state': fake.state(),
            'zipcode': fake.zipcode()
        }

        data.append(params)

    return _bulk_insert(Address, data, 'addresses')


@click.command()
def users():
    """
    Create random users.
    """
    data = []

    # Ensure we get about 50 unique random emails, +1 due to the seeded email.
    random_emails = [fake.email() for i in range(0, NUM_OF_FAKE_USERS-1)]
    random_emails.append(SEED_ADMIN_EMAIL)
    random_emails = list(set(random_emails))
    addresses = db.session.query(Address).all()

    for email in random_emails:
        params = {
            'role': 'member',
            'email': email,
            'password': User.encrypt_password('password'),
            'name': fake.name(),
            'locale': random.choice(ACCEPT_LANGUAGES),
            'address_id': (random.choice(addresses)).id
        }

        # Ensure the seeded admin is always an admin.
        if email == SEED_ADMIN_EMAIL:
            params['role'] = 'admin'
            params['locale'] = 'en'

        data.append(params)

    return _bulk_insert(User, data, 'users')


@click.command()
def issues():
    """
    Create random issues.
    """
    data = []

    for i in range(0, NUM_OF_FAKE_ISSUES):
        params = {
            'status': random.choice(Issue.STATUS.keys()),
            'label': random.choice(Issue.LABEL.keys()),
            'email': fake.email(),
            'question': fake.paragraph()
        }

        data.append(params)

    return _bulk_insert(Issue, data, 'issues')


@click.command()
def coupons():
    """
    Create random coupons.
    """
    data = []

    for i in range(0, NUM_OF_FAKE_COUPONS):
        random_pct = random.random()
        duration = random.choice(Coupon.DURATION.keys())

        # Create a fake unix timestamp in the future.
        redeem_by = fake.date_time_between(start_date='now',
                                           end_date='+1y').strftime('%s')

        # Bulk inserts need the same columns, so let's setup a few nulls.
        params = {
            'code': Coupon.random_coupon_code(),
            'duration': duration,
            'percent_off': None,
            'amount_off': None,
            'currency': None,
            'redeem_by': None,
            'max_redemptions': None,
            'duration_in_months': None,
        }

        if random_pct >= 0.5:
            params['percent_off'] = random.randint(1, 100)
            params['max_redemptions'] = random.randint(15, 50)
        else:
            params['amount_off'] = random.randint(1, 1337)
            params['currency'] = 'usd'

        if random_pct >= 0.75:
            params['redeem_by'] = redeem_by

        if duration == 'repeating':
            duration_in_months = random.randint(1, 12)
            params['duration_in_months'] = duration_in_months

        PaymentCoupon.create(**params)

        # Our database requires a Date object, not a unix timestamp.
        if redeem_by:
            params['redeem_by'] = datetime.utcfromtimestamp(float(redeem_by)) \
                .strftime('%Y-%m-%dT%H:%M:%S Z')

        if 'id' in params:
            params['code'] = params.get('id')
            del params['id']

        data.append(params)

    return _bulk_insert(Coupon, data, 'coupons')


@click.command()
def invoices():
    """
    Create random invoices.
    """
    data = []

    users = db.session.query(User).all()

    for user in users:
        for i in range(0, random.randint(1, 12)):
            # Create a fake unix timestamp in the future.
            created_on = fake.date_time_between(
                start_date='-1y', end_date='now').strftime('%s')
            period_start_on = fake.date_time_between(
                start_date='now', end_date='+1y').strftime('%s')
            period_end_on = fake.date_time_between(
                start_date=period_start_on, end_date='+14d').strftime('%s')
            exp_date = fake.date_time_between(
                start_date='now', end_date='+2y').strftime('%s')

            created_on = datetime.utcfromtimestamp(
                float(created_on)).strftime('%Y-%m-%dT%H:%M:%S Z')
            period_start_on = datetime.utcfromtimestamp(
                float(period_start_on)).strftime('%Y-%m-%d')
            period_end_on = datetime.utcfromtimestamp(
                float(period_end_on)).strftime('%Y-%m-%d')
            exp_date = datetime.utcfromtimestamp(
                float(exp_date)).strftime('%Y-%m-%d')

            plans = ['BRONZE', 'GOLD', 'PLATINUM']
            cards = ['Visa', 'Mastercard', 'AMEX',
                     'J.C.B', "Diner's Club"]

            params = {
                'created_on': created_on,
                'updated_on': created_on,
                'user_id': user.id,
                'receipt_number': fake.md5(),
                'description': '{0} MONTHLY'.format(random.choice(plans)),
                'period_start_on': period_start_on,
                'period_end_on': period_end_on,
                'currency': 'usd',
                'tax': random.random() * 100,
                'tax_percent': random.random() * 10,
                'total': random.random() * 1000,
                'brand': random.choice(cards),
                'last4': random.randint(1000, 9000),
                'exp_date': exp_date
            }

            data.append(params)

    return _bulk_insert(Invoice, data, 'invoices')


@click.command()
def businesses():
    """
    Create random businesses.
    """
    data = []

    # Ensure we get about 50 unique random emails, +1 due to the seeded email.
    addresses = db.session.query(Address).all()

    for i in range(0, NUM_OF_FAKE_BUSINESSES):

        open_time = fake.date_time_between(
            start_date='now', end_date='+1d').strftime('%s')
        close_time = fake.date_time_between(
            start_date=open_time, end_date='+1d').strftime('%s')

        open_time = datetime.utcfromtimestamp(
            float(open_time)).strftime('%Y-%m-%d %H:%M:%S')
        close_time = datetime.utcfromtimestamp(
            float(close_time)).strftime('%Y-%m-%d %H:%M:%S')

        params = {
            'name': fake.company(),
            'email': fake.company_email(),
            'type': random.choice(Business.TYPE.keys()),
            'open_time': open_time,
            'close_time': close_time,
            'phone': fake.phone_number(),
            'active': "1",
            'address_id': (random.choice(addresses)).id
        }

        data.append(params)

    return _bulk_insert(Business, data, 'businesses')


@click.command()
def occupancies():
    """
    Create random business occupanices.
    """
    data = []
    users = db.session.query(User).all()
    businesses = db.session.query(Business).all()

    for user in users:
        for i in range(0, random.randint(1, 12)):

            # Create a fake unix timestamp in the future.
            start_time = fake.date_time_between(
                start_date='now', end_date='+1d').strftime('%s')
            end_time = fake.date_time_between(
                start_date=start_time, end_date='+2d').strftime('%s')

            start_time = datetime.utcfromtimestamp(
                float(start_time)).strftime('%Y-%m-%d %H:%M:%S')
            end_time = datetime.utcfromtimestamp(
                float(end_time)).strftime('%Y-%m-%d %H:%M:%S')

            params = {
                'type': 'user',
                'start_time': start_time,
                'end_time': end_time,
                'user_id': user.id,
                'active': '1'
            }

            data.append(params)

    for business in businesses:
        for i in range(0, random.randint(1, 12)):

            # Create a fake unix timestamp in the future.
            start_time = fake.date_time_between(
                start_date='now', end_date='+1d').strftime('%s')
            end_time = fake.date_time_between(
                start_date=start_time, end_date='+2d').strftime('%s')

            start_time = datetime.utcfromtimestamp(
                float(start_time)).strftime('%Y-%m-%d %H:%M:%S')
            end_time = datetime.utcfromtimestamp(
                float(end_time)).strftime('%Y-%m-%d %H:%M:%S')

            params = {
                'type': 'business',
                'start_time': start_time,
                'end_time': end_time,
                'business_id': business.id,
                'active': '1'
            }

            data.append(params)

    return _bulk_insert(Occupancy, data, 'occupanices')


@click.command()
def employees():
    """
    Create random employees.
    """
    data = []
    users = db.session.query(User).all()
    businesses = db.session.query(Business).all()

    for business in businesses:
        admin_employee = random.choice(users)
        params = {
            'role': 'admin',
            'business_id': business.id,
            'user_id': admin_employee.id,
            'active': '1'
        }
        data.append(params)

        # Ensure that the member employee isnt the same as the admin employee
        member_employee = random.choice(db.session.query(User).filter(User.id != admin_employee.id).all())
        params = {
            'role': 'member',
            'business_id': business.id,
            'user_id': member_employee.id,
            'active': '1'
        }
        data.append(params)

    return _bulk_insert(Employee, data, 'employees')


@click.command()
@click.pass_context
def all(ctx):
    """
    Populate everything at once.

    :param ctx:
    :return: None
    """
    ctx.invoke(addresses)
    ctx.invoke(users)
    ctx.invoke(occupancies)
    ctx.invoke(issues)
    #ctx.invoke(coupons)
    ctx.invoke(invoices)
    ctx.invoke(businesses)
    ctx.invoke(employees)
    return None


cli.add_command(addresses)
cli.add_command(users)
cli.add_command(occupancies)
cli.add_command(issues)
#cli.add_command(coupons)
cli.add_command(invoices)
cli.add_command(businesses)
cli.add_command(employees)
cli.add_command(all)
