import logging
import random
from datetime import datetime, timedelta
import click
from faker import Faker
import pytz

from lyfeshoppe.app import create_app
from lyfeshoppe.extensions import db
from lyfeshoppe.blueprints.issue.models import Issue
from lyfeshoppe.blueprints.user.models import User
from lyfeshoppe.blueprints.common.models import Address
from lyfeshoppe.blueprints.business.models.business import Business, Employee, Product, Customer, Reservation

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

NUM_OF_FAKE_USERS = 20
NUM_OF_FAKE_ISSUES = 5
NUM_OF_FAKE_BUSINESSES = 10
MAX_EMPLOYEES_PER_BUSINESS = 5
MAX_CUSTOMERS_PER_BUSINESS = 10
MAX_PRODUCTS_PER_BUSINESS = 6
MAX_RESERVATIONS_PER_BUSINESS = 20


def generate_address():
    return Address(**{
                'street': fake.street_address(),
                'city': fake.city(),
                'state': fake.state(),
                'zipcode': fake.zipcode(),
                'district': fake.city(),
                'country': fake.country()
            }
        )


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
def users():
    """
    Create random users.
    """
    for i in xrange(0, NUM_OF_FAKE_USERS):
        params = {
            'email': fake.email(),
            'password': 'password',
            'name': fake.name(),
            'locale': random.choice(ACCEPT_LANGUAGES),
            'address': generate_address()
        }

        user = User(**params)
        user.save()

    _log_status(User.query.count(), "users")


@click.command()
def businesses():
    """
    Create random businesses.
    """

    for i in range(0, NUM_OF_FAKE_BUSINESSES):
        params = {
            'name': fake.company(),
            'email': fake.company_email(),
            'type': random.choice(Business.TYPE.keys()),
            'about': fake.paragraph(nb_sentences=6, variable_nb_sentences=True),
            'opening_time': datetime.strptime('08:00:00', '%H:%M:%S').time(),
            'closing_time': datetime.strptime('18:30:00', '%H:%M:%S').time(),
            'phone': fake.phone_number(),
            'active': "1",
            'weekends_open': random.choice(['0', '1']),
            'address': generate_address(),
            'metro': random.choice(Business.METRO.keys()),
            'website': 'https://lyfeshoppe.com',
            'twitter': 'https://twitter.com/TwitterSmallBiz',
            'facebook': 'https://www.facebook.com/LyfeShoppe-220689458262111',
            'youtube': 'https://www.youtube.com/channel/UCFv2NRs9s0vlgMdjCcWU9pQ',
            'linkedin': 'https://www.linkedin.com/in/mark-cuban-06a0755b'
        }

        business = Business(**params)
        business.save()

    _log_status(Business.query.count(), "businesses")


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
def employees():
    """
    Create random employees.
    """
    users = db.session.query(User).all()
    businesses = db.session.query(Business).all()

    for business in businesses:
        num_of_employees = random.randint(1, MAX_EMPLOYEES_PER_BUSINESS)

        users_list = list(users)
        to_be_employees = random.sample(users_list, num_of_employees)

        for user in to_be_employees:
            params = {
                'business_id': business.id,
                'user_id': user.id,
                'about': fake.paragraph(nb_sentences=6, variable_nb_sentences=True),
                'active': '1'
            }

            employee = Employee(**params)
            employee.save()

    _log_status(Employee.query.count(), "employees")


@click.command()
def products():
    """
    Create random products.
    """
    businesses = db.session.query(Business).all()

    for business in businesses:
        num_of_products = random.randint(0, MAX_PRODUCTS_PER_BUSINESS)

        employees = db.session.query(Employee).filter(Employee.business_id == business.id)
        employees_list = list(employees)
        if not employees_list:
            continue

        for i in range(0, num_of_products):
            params = {
                'name': fake.text(max_nb_chars=48),
                'category': random.choice(['Massage', 'Makeup', 'Nail', 'Haircut', 'Waxing']),
                'description': fake.paragraph(nb_sentences=6, variable_nb_sentences=True),
                'capacity': random.randint(1, 100),
                'price_cents': random.randint(100, 100000),
                'duration_mins': random.choice(['30', '60', '90', '120', '150', '180']),
                'business_id': business.id,
                'employees': random.sample(employees_list, random.randint(1, len(employees_list)))
            }
            product = Product(**params)
            product.save()

    _log_status(Product.query.count(), "products")


@click.command()
def customers():
    """
    Create random customers.
    """
    users = db.session.query(User).all()
    businesses = db.session.query(Business).all()

    for business in businesses:
        num_of_customers = random.randint(0, MAX_CUSTOMERS_PER_BUSINESS)

        users_list = list(users)
        to_be_customers = random.sample(users_list, num_of_customers)

        for user in to_be_customers:
            params = {
                'business_id': business.id,
                'user_id': user.id,
                'active': '1'
            }

            customer = Customer(**params)
            customer.save()

    _log_status(Customer.query.count(), "customers")


@click.command()
def reservations():
    """
    Create random reservations.
    """
    businesses = db.session.query(Business).all()
    for business in businesses:
        num_of_reservations = random.randint(0, MAX_RESERVATIONS_PER_BUSINESS)

        customers = db.session.query(Customer).filter(Customer.business_id == business.id).all()
        employees = db.session.query(Employee).filter(Employee.business_id == business.id).all()
        if not customers or not employees:
            continue

        for i in range(0, num_of_reservations):
            employee = random.choice(employees)

            # Solution from: http://stackoverflow.com/questions/23436095/querying-from-list-of-related-in-sqlalchemy-and-flask
            # Error hit: NotImplementedError: in_() not yet supported for relationships.
            # For a simple many-to-one, use in_() against the set of foreign key values.
            # Joins in SQLAlchemy is used
            products = Product.query.join(Product.employees).filter(Employee.id.in_(e.id for e in [employee])).all()
            if not products:
                continue
            product = random.choice(products)
            customer = random.choice(customers)

            # Create a fake unix timestamp in the future.
            duration = product.duration_mins
            start_time = random.choice([
                                    fake.date_time_this_month(before_now=True, after_now=False),
                                    fake.date_time_this_month(before_now=False, after_now=True)
                                ])
            end_time = start_time + timedelta(minutes=duration)

            if end_time < datetime.now():
                status = "executed"
            else:
                import copy
                statuses = copy.deepcopy(Reservation.STATUS)
                del statuses['executed']
                status = random.choice(statuses.keys())

            start_time = start_time.replace(tzinfo=pytz.utc)
            end_time = end_time.replace(tzinfo=pytz.utc)

            params = {
                'status': status,
                'start_time': start_time,
                'end_time': end_time,
                'business_id': business.id,
                'customer_id': customer.id,
                'employee_id': employee.id,
                'product_id': product.id
            }

            reservation = Reservation(**params)
            reservation.save()

    _log_status(Reservation.query.count(), "reservations")


@click.command()
@click.pass_context
def all(ctx):
    """
    Populate everything at once.

    :param ctx:
    :return: None
    """
    ctx.invoke(users)
    ctx.invoke(issues)
    ctx.invoke(businesses)
    ctx.invoke(employees)
    ctx.invoke(products)
    ctx.invoke(customers)
    ctx.invoke(reservations)
    return None


def generate_large_samples():
    global NUM_OF_FAKE_USERS
    global NUM_OF_FAKE_ISSUES
    global NUM_OF_FAKE_BUSINESSES
    global MAX_EMPLOYEES_PER_BUSINESS
    global MAX_CUSTOMERS_PER_BUSINESS
    global MAX_PRODUCTS_PER_BUSINESS
    global MAX_RESERVATIONS_PER_BUSINESS

    NUM_OF_FAKE_USERS = 200
    NUM_OF_FAKE_ISSUES = 5
    NUM_OF_FAKE_BUSINESSES = 100
    MAX_EMPLOYEES_PER_BUSINESS = 10
    MAX_CUSTOMERS_PER_BUSINESS = 40
    MAX_PRODUCTS_PER_BUSINESS = 20
    MAX_RESERVATIONS_PER_BUSINESS = 60


@click.command()
@click.pass_context
def large(ctx):
    """
    Populate everything at once.

    :param ctx:
    :return: None
    """
    generate_large_samples()

    ctx.invoke(users)
    ctx.invoke(issues)
    ctx.invoke(businesses)
    ctx.invoke(employees)
    ctx.invoke(products)
    ctx.invoke(customers)
    ctx.invoke(reservations)
    return None


def generate_very_large_samples():
    global NUM_OF_FAKE_USERS
    global NUM_OF_FAKE_ISSUES
    global NUM_OF_FAKE_BUSINESSES
    global MAX_EMPLOYEES_PER_BUSINESS
    global MAX_CUSTOMERS_PER_BUSINESS
    global MAX_PRODUCTS_PER_BUSINESS
    global MAX_RESERVATIONS_PER_BUSINESS

    NUM_OF_FAKE_USERS = 500
    NUM_OF_FAKE_ISSUES = 50
    NUM_OF_FAKE_BUSINESSES = 100
    MAX_EMPLOYEES_PER_BUSINESS = 10
    MAX_CUSTOMERS_PER_BUSINESS = 200
    MAX_PRODUCTS_PER_BUSINESS = 20
    MAX_RESERVATIONS_PER_BUSINESS = 400


@click.command()
@click.pass_context
def very_large(ctx):
    """
    Populate everything at once.

    :param ctx:
    :return: None
    """
    generate_very_large_samples()

    ctx.invoke(users)
    ctx.invoke(issues)
    ctx.invoke(businesses)
    ctx.invoke(employees)
    ctx.invoke(products)
    ctx.invoke(customers)
    ctx.invoke(reservations)
    return None


cli.add_command(users)
cli.add_command(issues)
cli.add_command(businesses)
cli.add_command(employees)
cli.add_command(products)
cli.add_command(customers)
cli.add_command(reservations)
cli.add_command(all)
cli.add_command(large)
cli.add_command(very_large)