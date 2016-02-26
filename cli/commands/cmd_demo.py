import random
from datetime import datetime, timedelta
import click
from faker import Faker
import pytz

from lyfeshoppe.app import create_app
from lyfeshoppe.extensions import db
from lyfeshoppe.blueprints.user.models import User
from lyfeshoppe.blueprints.business.models.business import Business, Employee, Product, Customer, Reservation, Review

fake = Faker()
app = create_app()
db.app = app

NUM_OF_EMPLOYEES = 10
NUM_OF_PRODUCTS = 20
FAKE_EMAIL_PREFIX = "f_"
MAX_CUSTOMERS_PER_BUSINESS = 100
MAX_RESERVATIONS_PER_BUSINESS = 2000
MAX_REVIEWS_PER_BUSINESS = 50


def generate_address():
    return {
        'country': "USA",
        'state': "CA",
        'city': "San Francisco",
        'zipcode': "94101",
        'street': "1001 Sunset Blvd.",
        'metro': "sf"
    }


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


@click.group()
def cli():
    """ Populate your db with generated data. """
    pass


@click.command()
def demo_user():
    """
    Create random users.
    """
    params = {
        'email': "demo@lyfeshoppe.com",
        'password': 'password',
        'first_name': "John",
        'last_name': "Smith",
        'phone': "2138805187",
        'locale': "en"
    }
    params.update(generate_address())
    del params['street']

    user = User(**params)
    user.save()

    _log_status(User.query.count(), "users")


@click.command()
def demo_business():
    """
    Create random businesses.
    """
    params = {
        'name': "Treases & Curls Hair Salon",
        'email': "demo-business@lyfeshoppe.com",
        'type': "hair",
        'about': "We are the best Hair Salon in San Francisco having won "
                 "multiple awards over the last 8 years of our operations."
                 " Visit us once & be a customer for life",
        'opening_time': datetime.strptime('08:00:00', '%H:%M:%S').time(),
        'closing_time': datetime.strptime('18:30:00', '%H:%M:%S').time(),
        'phone': "2138805187",
        'active': "1",
        'weekends_open': "1",
        'metro': "sf",
        'website': 'https://lyfeshoppe.com',
        'twitter': 'https://twitter.com/TwitterSmallBiz',
        'facebook': 'https://www.facebook.com/LyfeShoppe',
        'youtube': 'https://www.youtube.com/channel/UCFv2NRs9s0vlgMdjCcWU9pQ',
        'linkedin': 'https://www.linkedin.com/in/mark-cuban-06a0755b'
    }
    params.update(generate_address())

    business = Business(**params)
    business.save()

    _log_status(Business.query.count(), "businesses")


@click.command()
def demo_employees():
    """
    Create random employees.
    """
    business = db.session.query(Business).first()
    demo_user = db.session.query(User).filter(User.email == "demo@lyfeshoppe.com").first()
    main_employee_params = {
        'business_id': business.id,
        'user_id': demo_user.id,
        'about': fake.paragraph(nb_sentences=6, variable_nb_sentences=True),
        'active_employee': '1'
    }
    employee = Employee(**main_employee_params)
    employee.save()

    # Adding other employees
    for i in xrange(NUM_OF_EMPLOYEES):
        params = {
            'email': FAKE_EMAIL_PREFIX + fake.email(),
            'password': 'password',
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'phone': fake.phone_number(),
            'locale': "en"
        }
        params.update(generate_address())
        del params['street']

        user = User(**params)
        user = user.save()

        params = {
            'business_id': business.id,
            'user_id': user.id,
            'about': fake.paragraph(nb_sentences=6, variable_nb_sentences=True),
            'active_employee': '1'
        }

        employee = Employee(**params)
        employee.save()

    _log_status(Employee.query.count(), "employees")


@click.command()
def demo_products():
    """
    Create random products.
    """
    business = db.session.query(Business).first()
    employees = list(db.session.query(Employee).filter(Employee.business_id == business.id))

    for i in xrange(NUM_OF_PRODUCTS):
        params = {
            'name': fake.text(max_nb_chars=48),
            'category': random.choice(['Massage', 'Makeup', 'Nail', 'Haircut', 'Waxing']),
            'description': fake.paragraph(nb_sentences=6, variable_nb_sentences=True),
            'price': random.randint(10, 1000),
            'duration_mins': random.choice(['30', '60', '90', '120', '150', '180']),
            'business_id': business.id,
            'employees': random.sample(employees, random.randint(1, len(employees)))
        }
        product = Product(**params)
        product.save()

    _log_status(Product.query.count(), "products")


@click.command()
def demo_customers():
    """
    Create random customers.
    """
    business = db.session.query(Business).first()
    for i in xrange(NUM_OF_EMPLOYEES):
        params = {
            'email': FAKE_EMAIL_PREFIX + fake.email(),
            'password': 'password',
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'phone': fake.phone_number(),
            'locale': "en"
        }
        params.update(generate_address())
        del params['street']

        user = User(**params)
        user = user.save()

        params = {
            'business_id': business.id,
            'user_id': user.id,
            'active_customer': '1'
        }

        customer = Customer(**params)
        customer.save()

    _log_status(Customer.query.count(), "customers")


@click.command()
@click.pass_context
def all(ctx):
    """
    Populate everything at once.

    :param ctx:
    :return: None
    """
    ctx.invoke(demo_user)
    ctx.invoke(demo_business)
    ctx.invoke(demo_employees)
    ctx.invoke(demo_products)
    ctx.invoke(demo_customers)
    return None


cli.add_command(demo_user)
cli.add_command(demo_business)
cli.add_command(demo_employees)
cli.add_command(demo_products)
cli.add_command(demo_customers)
cli.add_command(all)
