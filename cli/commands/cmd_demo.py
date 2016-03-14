import random
from datetime import datetime, timedelta
import click
from faker import Faker
import pytz
import copy

from config import settings
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
NUM_OF_CUSTOMERS = 100
NUM_OF_RESERVATIONS = 2000
NUM_OF_REVIEWS = 50

PRODUCTS = [
    {
        'num': 1,
        'name': 'Root Touchup',
        'category': 'Hair Color',
        'description': 'Color is applied only to the most recent section of re-growth. Usually the first inch of hair from the scalp. Generally those getting root touch-ups get this service repeated every 4-6 weeks as the natural color grows in and becomes apparent.',
        'price': 60,
        'duration_mins': 45
    },
    {
        'num': 2,
        'name': 'All over color',
        'category': 'Hair Color',
        'description': 'This is for individual who desires for all of their hair to be a different solid color.',
        'price': 180,
        'duration_mins': 90
    },
    {
        'num': 3,
        'name': 'Partial Weave',
        'category': 'Hair Color',
        'description': 'Partial weaves involve the common weaving method where majority of the hair is braided leaving a thin section at the top for parting, on the sides and possibly the back as well to allow for wearing of high ponytails.',
        'price': 160,
        'duration_mins': 90
    },
    {
        'num': 4,
        'name': 'Full Weave',
        'category': 'Hair Color',
        'description': 'A full weave is when all your hair has been braided up and extension hair is applied over your own.',
        'price': 240,
        'duration_mins': 120
    },
    {
        'num': 5,
        'name': 'Roots & Partial Weave',
        'category': 'Hair Color',
        'description': 'Root touch up with Partial hair weave.',
        'price': 320,
        'duration_mins': 120
    },
    {
        'num': 6,
        'name': 'Roots & Full Weave',
        'category': 'Hair Color',
        'description': 'Root touch up with Full hair weave.',
        'price': 400,
        'duration_mins': 150
    },
    {
        'num': 7,
        'name': "Men's Haircut",
        'category': 'Hair Cut',
        'description': "Men's haircut performed as requested by the client.",
        'price': 20,
        'duration_mins': 30
    },
    {
        'num': 8,
        'name': "Women's Dry Haircut",
        'category': 'Hair Cut',
        'description': "Women's dry haircut performed as requested by the client.",
        'price': 25,
        'duration_mins': 30
    },
    {
        'num': 9,
        'name': "Senior's OR Kids Haircut",
        'category': 'Hair Cut',
        'description': "Hair cut for Seniors over 60 or kids below 12 .",
        'price': 15,
        'duration_mins': 20
    },
    {
        'num': 10,
        'name': "Toddler's Haircut",
        'category': 'Hair Cut',
        'description': "Toddler's haircut performed as requested by the client.",
        'price': 10,
        'duration_mins': 15
    },
    {
        'num': 11,
        'name': "Women's Straightening & Haircut",
        'category': 'Hair Cut',
        'description': "Great for women with curly or wavy hair. This service provides hair straightening and cutting in a combo pack.",
        'price': 45,
        'duration_mins': 30
    },
    {
        'num': 12,
        'name': "Women's Shampoo Cut & Style",
        'category': 'Hair Cut',
        'description': "Hair cut, shampooing and styling done to provide a complete hair style makeover for every occasion.",
        'price': 60,
        'duration_mins': 45
    },
    {
        'num': 13,
        'name': "Bridal Hairdo",
        'category': 'Specials',
        'description': "Exquisite bridal services provided for you to look great on your wedding day.",
        'price': 360,
        'duration_mins': 150
    },
    {
        'num': 14,
        'name': "Chic Party Styling",
        'category': 'Specials',
        'description': "Fun and Fresh styles from our brochure to help you look great at every party.",
        'price': 240,
        'duration_mins': 120
    },
    {
        'num': 15,
        'name': "Formal Hairdo",
        'category': 'Specials',
        'description': "Modern day formal look lets you help look great in the corporate world.",
        'price': 120,
        'duration_mins': 45
    },
    {
        'num': 16,
        'name': "Brazilian Waxing",
        'category': 'Waxing',
        'description': "Complete brazilian waxing service in a private room.",
        'price': 180,
        'duration_mins': 30
    },
    {
        'num': 17,
        'name': "Arm OR Leg Waxing",
        'category': 'Waxing',
        'description': "Complete arms or leg waxing service.",
        'price': 60,
        'duration_mins': 30
    },
    {
        'num': 18,
        'name': "Manicure",
        'category': 'Nails Service',
        'description': "Complete manicure service.",
        'price': 40,
        'duration_mins': 30
    },
    {
        'num': 19,
        'name': "Pedicure",
        'category': 'Nails Service',
        'description': "Complete pedicure service.",
        'price': 60,
        'duration_mins': 45
    },
    {
        'num': 20,
        'name': "Shellac Nail Paint",
        'category': 'Nails Service',
        'description': "Nail Paint & styling done to perfection.",
        'price': 100,
        'duration_mins': 45
    },

]

#'Massage', 'Makeup', 'Nail', 'Haircut', 'Waxing'

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
    Create random user.
    """
    params = {
        'email': settings.DEMO_EMAIL,
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
    demo_user = db.session.query(User).filter(User.email == settings.DEMO_EMAIL).first()
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
            'name': PRODUCTS[i].get('name', "Fake product"),
            'category': PRODUCTS[i].get('category', "Fake Category"),
            'description': PRODUCTS[i].get('description', "Fake product description"),
            'price': PRODUCTS[i].get('price', 100),
            'duration_mins': PRODUCTS[i].get('duration_mins', 60),
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
    for i in xrange(NUM_OF_CUSTOMERS):
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
def demo_reviews():
    """
    Create random reviews.
    """
    business = db.session.query(Business).first()

    customers = db.session.query(Customer).filter(Customer.business_id == business.id).all()
    employees = db.session.query(Employee).filter(Employee.business_id == business.id).all()

    for i in xrange(NUM_OF_REVIEWS):
        employee = random.choice(employees)

        # Solution from:
        # http://stackoverflow.com/questions/23436095/querying-from-list-of-related-in-sqlalchemy-and-flask
        # Error hit: NotImplementedError: in_() not yet supported for relationships.
        # For a simple many-to-one, use in_() against the set of foreign key values.
        # Joins in SQLAlchemy is used
        products = Product.query.join(Product.employees).filter(Employee.id.in_(e.id for e in [employee])).all()
        if not products:
            continue
        product = random.choice(products)
        customer = random.choice(customers)

        params = {
            'status': random.choice(Review.STATUS.keys()),
            'description': fake.paragraph(nb_sentences=6, variable_nb_sentences=True),
            'business_id': business.id,
            'customer_id': customer.id,
            'employee_id': employee.id,
            'product_id': product.id
        }

        review = Review(**params)
        review.save()

    _log_status(Review.query.count(), "reviews")



@click.command()
def demo_reservations():
    """
    Create random reservations.
    """
    business = db.session.query(Business).first()
    customers = db.session.query(Customer).filter(Customer.business_id == business.id).all()
    employees = db.session.query(Employee).filter(Employee.business_id == business.id).all()

    statuses = copy.deepcopy(Reservation.STATUS)
    del statuses['executed']

    for i in xrange(NUM_OF_RESERVATIONS):
        employee = random.choice(employees)

        # Solution from:
        # http://stackoverflow.com/questions/23436095/querying-from-list-of-related-in-sqlalchemy-and-flask
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

        status = "executed" if end_time < datetime.now() else random.choice(statuses.keys())
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
    ctx.invoke(demo_user)
    ctx.invoke(demo_business)
    ctx.invoke(demo_employees)
    ctx.invoke(demo_products)
    ctx.invoke(demo_customers)
    ctx.invoke(demo_reviews)
    ctx.invoke(demo_reservations)
    return None


cli.add_command(demo_user)
cli.add_command(demo_business)
cli.add_command(demo_employees)
cli.add_command(demo_products)
cli.add_command(demo_customers)
cli.add_command(demo_reviews)
cli.add_command(demo_reservations)
cli.add_command(all)
