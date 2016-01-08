import logging
import random
from datetime import datetime
import click
from faker import Faker

from lyfeshoppe.app import create_app
from lyfeshoppe.extensions import db
from lyfeshoppe.blueprints.user.models import User
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

NUM_OF_FAKE_USERS = 50
NUM_OF_FAKE_BUSINESSES = 200
MAX_CUSTOMERS_PER_BUSINESS = 50
MAX_PRODUCTS_PER_BUSINESS = 30
MAX_EMPLOYEES_PER_BUSINESS = 10


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


address = {
    'street': fake.street_address(),
    'city': fake.city(),
    'state': fake.state(),
    'zipcode': fake.zipcode(),
    'district': fake.city(),
    'country': fake.country()
}


@click.command()
def users():
    """
    Create random users.
    """
<<<<<<< HEAD
    for i in range(0, NUM_OF_FAKE_USERS):
        user_params = {
            'email': fake.email(),
            'password': User.encrypt_password('fakepassword'),
=======
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
>>>>>>> parent of 1d6dd10... changed test data password
            'name': fake.name(),
            'locale': random.choice(ACCEPT_LANGUAGES)
        }

        u = User(**user_params)
        u.save()

    admin_user_params = {
        'email': "dev@localhost.com",
        'password': User.encrypt_password('fakepassword'),
        'name': "Harshit Imudianda",
        'locale': 'en',
        'role': 'admin'
    }

    u = User(**admin_user_params)
    u.save()

    _log_status(User.query.count(), 'users')


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
            'address': address,
            'metro': random.choice(Business.METRO.keys()),
            'website': 'https://lyfeshoppe.com',
            'twitter': 'https://twitter.com/TwitterSmallBiz',
            'facebook': 'https://www.facebook.com/LyfeShoppe-220689458262111',
            'youtube': 'https://www.youtube.com/channel/UCFv2NRs9s0vlgMdjCcWU9pQ',
            'linkedin': 'https://www.linkedin.com/in/mark-cuban-06a0755b'
        }

        Business.get_or_create(params)
    _log_status(Business.query.count(), 'businesses')


@click.command()
def customers():
    """
    Create random customers.
    """
    data = []

    user_ids = list(db.session.query(User.id).distinct())
    business_ids = list(db.session.query(Business.id).distinct())

    for business_id in business_ids:
        num_of_customers = random.randint(0, MAX_CUSTOMERS_PER_BUSINESS)
        to_be_customers = random.sample(user_ids, num_of_customers)

        for user_id in to_be_customers:
            params = {
                'business_id': business_id,
                'user_id': user_id,
                'active': '1'
            }
            data.append(params)

    return _bulk_insert(Customer, data, 'customers')


@click.command()
def products():
    """
    Create random products.
    """
    data = []
    business_ids = list(db.session.query(Business.id).distinct())

    for business_id in business_ids:
        num_of_products = random.randint(0, MAX_PRODUCTS_PER_BUSINESS)

        for i in range(0, num_of_products):
            params = {
                'name': fake.text(max_nb_chars=48),
                'category': random.choice(['Massage', 'Makeup', 'Nail', 'Haircut', 'Waxing']),
                'description': fake.paragraph(nb_sentences=6, variable_nb_sentences=True),
                'capacity': random.randint(1, 100),
                'price_cents': random.randint(100, 100000),
                'duration_mins': random.randint(10, 180),
                'business_id': business_id
            }

            data.append(params)

    return _bulk_insert(Product, data, 'products')


@click.command()
def employees():
    """
    Create random employees.
    """
    data = []
    user_ids = list(db.session.query(User.id).distinct())
    business_ids = list(db.session.query(Business.id).distinct())

    for business_id in business_ids:
        products = Product.query.filter(Product.business_id == business_id).all()

        num_of_employees = random.randint(0, MAX_EMPLOYEES_PER_BUSINESS)
        to_be_employees = random.sample(user_ids, num_of_employees)

        for user_id in to_be_employees:
            num_of_products_per_employee = random.randint(0, len(products))
            params = {
                'business_id': business_id,
                'user_id': user_id,
                'products': random.sample(list(products), num_of_products_per_employee),
                'about': fake.paragraph(nb_sentences=6, variable_nb_sentences=True),
                'active': '1'
            }
            data.append(params)

    return _bulk_insert(Employee, data, 'employees')


@click.command()
def reservations():
    """
    Create random reservations.
    """
    data = []
    business_ids = db.session.query(Business.id).distinct()

    MAX_RESERVATIONS_PER_BUSINESS = 200

    for business_id in business_ids:
        business_id = business_id[0]

        num_of_reservations = random.randint(0, MAX_RESERVATIONS_PER_BUSINESS)
        if not num_of_reservations:
            continue

        customer_ids = db.session.query(Customer.id).filter(Customer.business_id == business_id).distinct()
        employee_ids = db.session.query(Employee.id).filter(Employee.business_id == business_id).distinct()
        product_ids = db.session.query(Product.id).filter(Product.business_id == business_id).distinct()

        if not customer_ids.count() or not employee_ids.count() or not product_ids.count():
            continue

        for i in range(0, num_of_reservations):
            params = {
                'business_id': business_id,
                'customer_id': random.choice(list(customer_ids))[0],
                'product_id': random.choice(list(product_ids))[0],
                'employee_id': random.choice(list(employee_ids))[0]
            }
            data.append(params)

    return _bulk_insert(Reservation, data, 'reservations')


@click.command()
@click.pass_context
def all(ctx):
    """
    Populate everything at once.

    :param ctx:
    :return: None
    """
    ctx.invoke(users)
    ctx.invoke(businesses)
    ctx.invoke(products)
    ctx.invoke(employees)
    ctx.invoke(customers)
    ctx.invoke(reservations)
    return None


cli.add_command(users)
cli.add_command(businesses)
cli.add_command(products)
cli.add_command(employees)
cli.add_command(customers)
cli.add_command(reservations)
cli.add_command(all)
