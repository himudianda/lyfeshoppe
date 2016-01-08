import logging
import random
from datetime import datetime
import click
from faker import Faker

from lyfeshoppe.app import create_app
from lyfeshoppe.extensions import db
from lyfeshoppe.blueprints.user.models import User
from lyfeshoppe.blueprints.common.models import Availability, Occupancy
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
NUM_OF_FAKE_RESERVATIONS = 10000


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
    for i in range(0, NUM_OF_FAKE_USERS):
        user_params = {
            'email': fake.email(),
            'password': User.encrypt_password('fakepassword'),
            'name': fake.name(),
            'locale': random.choice(ACCEPT_LANGUAGES),
            'address': address
        }

        User.get_or_create(user_params)

    admin_user_params = {
        'email': SEED_ADMIN_EMAIL,
        'password': User.encrypt_password('fakepassword'),
        'name': "Harshit Imudianda",
        'locale': 'en',
        'role': 'admin',
        'address': address
    }

    User.get_or_create(admin_user_params)
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
def occupancies():
    """
    Create random business occupanices.
    """
    data = []

    users = db.session.query(User).all()
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
                'business_id': None,
                'active': '1'
            }

            data.append(params)

    businesses = db.session.query(Business).all()
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
                'user_id': None,
                'business_id': business.id,
                'active': '1'
            }

            data.append(params)

    return _bulk_insert(Occupancy, data, 'occupancies')


@click.command()
def customers():
    """
    Create random customers.
    """
    data = []
    users = db.session.query(User).all()
    businesses = db.session.query(Business).all()

    for business in businesses:
        params = {
            'business_id': business.id,
            'user_id': (random.choice(users)).id,
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
    businesses = db.session.query(Business).all()

    for business in businesses:
        for i in range(0, random.randint(1, 10)):
            params = {
                'name': fake.text(max_nb_chars=48),
                'category': random.choice(['Massage', 'Makeup', 'Nail', 'Haircut', 'Waxing']),
                'description': fake.paragraph(nb_sentences=6, variable_nb_sentences=True),
                'capacity': random.randint(1, 100),
                'price_cents': random.randint(100, 100000),
                'duration_mins': random.randint(10, 180),
                'business_id': business.id
            }

            data.append(params)

    return _bulk_insert(Product, data, 'products')


@click.command()
def employees():
    """
    Create random employees.
    """
    data = []
    businesses = db.session.query(Business).all()

    for business in businesses:
        employees_list = []
        for i in range(0, random.randint(12, 20)):

            if len(employees_list):
                admin_employee = random.choice(
                    db.session.query(User).filter(~User.id.in_(employees_list)).all()
                )
            else:
                admin_employee = random.choice(
                    db.session.query(User).all()
                )
            employees_list.append(admin_employee.id)
            params = {
                'role': 'admin',
                'business_id': business.id,
                'user_id': admin_employee.id,
                'products': Product.query.filter(Product.business_id == business.id).all(),
                'about': fake.paragraph(nb_sentences=6, variable_nb_sentences=True),
                'active': '1'
            }
            data.append(params)

            # Ensure that the member employee isnt the same as the admin employee
            member_employee = random.choice(
                db.session.query(User).filter(~User.id.in_(employees_list)).all()
            )
            employees_list.append(member_employee.id)
            params = {
                'role': 'member',
                'business_id': business.id,
                'user_id': member_employee.id,
                'products': Product.query.filter(Product.business_id == business.id).all(),
                'about': fake.paragraph(nb_sentences=6, variable_nb_sentences=True),
                'active': '1'
            }
            data.append(params)

    return _bulk_insert(Employee, data, 'employees')


@click.command()
def employee_product_relations():
    """
    Create random employee_product_relations.
    """
    products = db.session.query(Product).all()

    for product in products:
        product.employees.extend(Employee.query.filter(Employee.business_id == product.business_id).all())
        product.save()


@click.command()
def availabilities():
    """
    Create random product availabilities.
    """
    data = []

    products = db.session.query(Product).all()
    for product in products:
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
                'type': 'product',
                'start_time': start_time,
                'end_time': end_time,
                'product_id': product.id,
                'active': '1'
            }

            data.append(params)

    return _bulk_insert(Availability, data, 'availabilities')


@click.command()
def reservations():
    """
    Create random reservations.
    """
    data = []

    for business in db.session.query(Business).all():
        customers = db.session.query(Customer).filter(Customer.business_id == business.id).all()
        employees = db.session.query(Employee).filter(Employee.business_id == business.id).all()
        products = db.session.query(Product).filter(Product.business_id == business.id).all()

        # Create a fake unix timestamp in the future.
        start_time = fake.date_time_between(
            start_date='now', end_date='+1d').strftime('%s')
        end_time = fake.date_time_between(
            start_date=start_time, end_date='+2d').strftime('%s')

        start_time = datetime.utcfromtimestamp(
            float(start_time)).strftime('%Y-%m-%d %H:%M:%S')
        end_time = datetime.utcfromtimestamp(
            float(end_time)).strftime('%Y-%m-%d %H:%M:%S')

        for i in range(0, 20):
            params = {
                'status': random.choice(Reservation.STATUS.keys()),
                'start_time': start_time,
                'end_time': end_time,
                'business_id': business.id,
                'customer_id': (random.choice(customers)).id,
                'employee_id': (random.choice(employees)).id,
                'product_id': (random.choice(products)).id
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
    ctx.invoke(occupancies)
    ctx.invoke(employees)
    ctx.invoke(products)
    ctx.invoke(employee_product_relations)
    ctx.invoke(availabilities)
    ctx.invoke(customers)
    ctx.invoke(reservations)
    return None


cli.add_command(users)
cli.add_command(businesses)
cli.add_command(occupancies)
cli.add_command(employees)
cli.add_command(products)
cli.add_command(employee_product_relations)
cli.add_command(availabilities)
cli.add_command(customers)
cli.add_command(reservations)
cli.add_command(all)
