from collections import OrderedDict
from sqlalchemy import or_, UniqueConstraint
import pytz
import os
import math
from sqlalchemy.ext.declarative import declared_attr

from config.settings import STATIC_FILES_PATH
from flask_login import current_user
from lyfeshoppe.lib.util_sqlalchemy import ResourceMixin, AwareDateTime
from lyfeshoppe.blueprints.common.models import Address, Occupancy, Availability
from lyfeshoppe.blueprints.user.models import User
from lyfeshoppe.extensions import db


class Review(ResourceMixin, db.Model):
    __tablename__ = 'reviews'

    STATUS = OrderedDict([
        ('poor', 'Poor.'),
        ('expected_more', 'Expected More.'),
        ('average', 'Average.'),
        ('good', 'Good.'),
        ('very_good', 'Very Good.')
    ])

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(
                db.Enum(*STATUS, name='review_statuses'), index=True, nullable=False, server_default='very_good')
    description = db.Column(db.Text())

    # Relationships
    customer_id = db.Column(db.Integer, db.ForeignKey(
                        'customers.id', onupdate='CASCADE', ondelete='CASCADE'
                    ), index=True, nullable=False)
    business_id = db.Column(db.Integer, db.ForeignKey(
                        'businesses.id', onupdate='CASCADE', ondelete='CASCADE'
                    ), index=True, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey(
                        'employees.id', onupdate='CASCADE', ondelete='CASCADE'
                    ), index=True, nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey(
                        'products.id', onupdate='CASCADE', ondelete='CASCADE'
                    ), index=True, nullable=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(Review, self).__init__(**kwargs)

    @classmethod
    def search(cls, query):
        """
        Search a resource by 1 or more fields.

        :param query: Search query
        :type query: str
        :return: SQLAlchemy filter
        """
        if not query:
            return ''

        search_query = '%{0}%'.format(query)
        search_chain = cls.description.ilike(search_query)

        return search_chain

    @classmethod
    def create_from_form(cls, business_id, employee_id, customer_id, form):
        """
        Return whether or not the product was created successfully.

        :return: bool
        """

        review = Review()
        form.populate_obj(review)

        if review.product_id == "":
            review.product_id = None
        review.business_id = business_id
        review.employee_id = employee_id
        review.customer_id = customer_id
        review.save()
        return True


class Reservation(ResourceMixin, db.Model):
    __tablename__ = 'reservations'

    STATUS = OrderedDict([
        ('new', 'Unconfirmed reservation.'),
        ('confirmed', 'Confirmed reservation.'),
        ('cancelled', 'Cancelled reservation.'),
        ('executed', 'Completed reservation.')
    ])

    STATUS_COLORS = OrderedDict([
        ('new', 'yellow'),
        ('confirmed', 'green'),
        ('cancelled', 'red'),
        ('executed', 'blue')
    ])

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum(*STATUS, name='reservation_statuses'), index=True, nullable=False, server_default='new')
    start_time = db.Column(AwareDateTime())
    end_time = db.Column(AwareDateTime())

    # Relationships
    customer_id = db.Column(db.Integer, db.ForeignKey(
                        'customers.id', onupdate='CASCADE', ondelete='CASCADE'
                    ), index=True, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey(
                        'employees.id', onupdate='CASCADE', ondelete='CASCADE'
                    ), index=True, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(
                        'products.id', onupdate='CASCADE', ondelete='CASCADE'
                    ), index=True, nullable=False)
    business_id = db.Column(db.Integer, db.ForeignKey(
                        'businesses.id', onupdate='CASCADE', ondelete='CASCADE'
                    ), index=True, nullable=False)

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(Reservation, self).__init__(**kwargs)

    @classmethod
    def create(cls, params):
        """
        Return whether or not the employee was created successfully.

        :return: bool
        """

        if 'start_time' in params:
            if params.get('start_time') is not None:
                params['start_time'] = params.get('start_time').replace(
                    tzinfo=pytz.UTC)

        if 'end_time' in params:
            if params.get('end_time') is not None:
                params['end_time'] = params.get('end_time').replace(
                    tzinfo=pytz.UTC)

        business_id = params['business_id']
        customer_email = params.pop("customer_email", None)

        customer = Customer.get_or_create(business_id, customer_email)
        params['customer_id'] = str(customer.id)

        reservation = cls(**params)
        reservation.save()
        return True


class CustomerAndEmployeeMixin(object):

    # Refer notes below:
    # http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/mixins.html
    @declared_attr
    def business_id(cls):
        return db.Column(db.Integer, db.ForeignKey(
                        'businesses.id', onupdate='CASCADE', ondelete='CASCADE'
                    ), index=True, nullable=False)

    # Many to One relationship: Many customers can have same user
    # Thats becoz; A customer can belong with multiple businesses.
    # http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html
    # Also refer these notes for the syntax below:
    # http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/mixins.html
    @declared_attr
    def user_id(cls):
        return db.Column(db.Integer, db.ForeignKey(
                        'users.id', onupdate='CASCADE', ondelete='CASCADE'
                        ), index=True, nullable=False)

    # @declared_attr
    # def user(cls):
    #    return db.relationship(User)

    @classmethod
    def search(cls, query):
        """
        Search a resource by 1 or more fields.

        :param query: Search query
        :type query: str
        :return: SQLAlchemy filter
        """
        if not query:
            return ''

        search_query = '%{0}%'.format(query)
        users = User.query.filter(or_(User.email.ilike(search_query), User.name.ilike(search_query)))
        user_ids = [user.id for user in users]

        search_chain = (cls.user_id.in_(user_ids))
        return search_chain

    @classmethod
    def find_by_identity(cls, business_id, identity):
        """
        Find a resource by their e-mail or username.

        :param identity: Email or username
        :type identity: str
        :return: User instance
        """
        user = User.query.filter((User.email == identity) | (User.username == identity)).first()
        if not user:
            return None
        return cls.query.filter(cls.user == user, cls.business_id == business_id)

    @classmethod
    def get_or_create(cls, **kwargs):
        business_id = kwargs.get('business_id')

        user = User.find_by_identity(kwargs.get('email'))
        if not user:
            user = User.create(name=kwargs.get('name'), email=kwargs.get('email'))

        obj = cls.query.filter(
                        cls.user == user, cls.business_id == business_id
                    ).first()
        if obj:
            return (obj, False)  # Customer OR Employee exists & wasnt created

        obj = cls()
        obj.business_id = business_id
        obj.user = user
        obj = obj.save()
        return (obj, True)  # New Customer OR Employee was created

    @classmethod
    def get_or_create_from_form(cls, business_id, form):
        """
        Return whether or not the resource was created successfully.

        :return: bool
        """
        new_obj = cls()
        form.populate_obj(new_obj)

        user = User.find_by_identity(new_obj.email)
        if not user:
            user = User.create_from_form(form)

        obj = cls.query.filter(
                    cls.user == user, cls.business_id == business_id
                ).first()
        if obj:
            return (obj, False)  # Customer OR Employee already exists

        obj = cls()
        form.populate_obj(obj)
        obj.business_id = business_id
        obj.user = user
        obj = obj.save()
        return (obj, True)  # New customer or employee was created


class Customer(ResourceMixin, CustomerAndEmployeeMixin, db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    reservations = db.relationship(Reservation, backref='customer', passive_deletes=True)
    reviews = db.relationship(Review, backref='customer', passive_deletes=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    __table_args__ = (UniqueConstraint('user_id', 'business_id', name='_customer_user_business_uc'), )

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(Customer, self).__init__(**kwargs)

    def modify_from_form(self, form):
        """
        Return whether or not the customer was modified successfully.

        :return: bool
        """

        form.populate_obj(self)
        form.populate_obj(self.user)
        # Create Business Address if it dint exist previously
        if not self.user.address:
            self.user.address = Address()
        form.populate_obj(self.user.address)

        self.save()

        return True

    @property
    def num_of_reservations(self):
        # Refer notes under Using EXISTS topic under link
        # http://docs.sqlalchemy.org/en/latest/orm/tutorial.html
        return Reservation.query.filter(Reservation.customer_id == self.id).count()
        # NOTE: below is an example of using any() & it also works. But the above statment
        # is easier to use & understand
        # return Reservation.query.filter(Reservation.employee.has(Employee.id == self.id)).count()


employee_product_relations = db.Table(
    'employee_product_relations',
    # NOTE: businesses.id & users.id are used because businesses & users are the table names
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), nullable=False),
    db.Column('employee_id', db.Integer, db.ForeignKey('employees.id'), nullable=False),
    db.PrimaryKeyConstraint('product_id', 'employee_id')
)


class EmployeeProductRelationships(object):
    def __init__(self, product_id, employee_id):
        self.product_id = product_id
        self.employee_id = employee_id

db.mapper(EmployeeProductRelationships, employee_product_relations)


class Employee(ResourceMixin, CustomerAndEmployeeMixin, db.Model):
    __tablename__ = 'employees'

    ROLE = OrderedDict([
        ('admin', 'Admin'),  # Admin employees have full access to Business backends
        ('member', 'Member')  # Member employees only have access to products in a Business that they offer
    ])

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Enum(*ROLE, name='employee_roles'), index=True, nullable=False, server_default='member')
    about = db.Column(db.Text())

    products = db.relationship('Product', secondary=employee_product_relations, backref='employees')
    reservations = db.relationship(Reservation, backref='employee', passive_deletes=True)
    reviews = db.relationship(Review, backref='employee', passive_deletes=True)

    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    __table_args__ = (UniqueConstraint('user_id', 'business_id', name='_employee_user_business_uc'), )

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(Employee, self).__init__(**kwargs)

    def modify_from_form(self, form):
        """
        Return whether or not the employee was modified successfully.

        :return: bool
        """

        form.populate_obj(self)
        form.populate_obj(self.user)
        # Create Business Address if it dint exist previously
        if not self.user.address:
            self.user.address = Address()
        form.populate_obj(self.user.address)

        self.save()

        return True

    @property
    def num_of_products(self):
        # Refer notes under Using EXISTS topic under link
        # http://docs.sqlalchemy.org/en/latest/orm/tutorial.html
        return Product.query.filter(Product.employees.any(Employee.id == self.id)).count()

    @property
    def num_of_reservations(self):
        # Refer notes under Using EXISTS topic under link
        # http://docs.sqlalchemy.org/en/latest/orm/tutorial.html
        return Reservation.query.filter(Reservation.employee_id == self.id).count()
        # NOTE: below is an example of using any() & it also works. But the above statment
        # is easier to use & understand
        # return Reservation.query.filter(Reservation.employee.has(Employee.id == self.id)).count()

    @property
    def total_sales(self):
        total_sales_in_cents = sum([item.product.price_cents for item in self.reservations])
        total_sales = total_sales_in_cents/100
        return total_sales

    @property
    def rating(self):
        rating_num = 0.0  # This should be float & not int for correct results to be computed below
        for review in self.reviews:
            rating_num += (Review.STATUS.keys().index(review.status) + 1)
        if rating_num == 0:
            return rating_num
        return int(math.ceil(rating_num/len(self.reviews)))


class Product(ResourceMixin, db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    category = db.Column(db.String(32))
    description = db.Column(db.Text())
    capacity = db.Column(db.Integer, nullable=False, default=1)  # 1 person
    price_cents = db.Column(db.Integer, nullable=False, default=1000)  # $10
    duration_mins = db.Column(db.Integer, nullable=False, default=60)  # 1 hour

    # Relationships.
    business_id = db.Column(db.Integer, db.ForeignKey(
                        'businesses.id', onupdate='CASCADE', ondelete='CASCADE'
                    ), index=True, nullable=False)
    availabilities = db.relationship(Availability, backref="product")
    reservations = db.relationship(Reservation, backref='product', passive_deletes=True)
    reviews = db.relationship(Review, backref='product', passive_deletes=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(Product, self).__init__(**kwargs)

    @classmethod
    def search(cls, query):
        """
        Search a resource by 1 or more fields.

        :param query: Search query
        :type query: str
        :return: SQLAlchemy filter
        """
        if not query:
            return ''

        search_query = '%{0}%'.format(query)
        search_chain = (cls.name.ilike(search_query),
                        cls.description.ilike(search_query))

        return or_(*search_chain)

    @classmethod
    def create_from_form(cls, business_id, form):
        """
        Return whether or not the product was created successfully.

        :return: bool
        """

        product = cls()
        form.populate_obj(product)
        product.business_id = business_id
        product.save()
        return True

    def modify_from_form(self, form):
        """
        Return whether or not the product was modified successfully.

        :return: bool
        """

        form.populate_obj(self)
        self.save()

        return True


class Business(ResourceMixin, db.Model):
    __tablename__ = 'businesses'

    SERVICES = OrderedDict([
        ('beauty', 'Beauty'),
        ('health', 'Health & Fitness'),
        ('entertainment', 'Entertainment'),
        ('sport', 'Sports'),
        ('lessons', 'Educational'),
        ('home', 'Home'),
        ('auto', 'Auto'),
        ('personal', 'Personal Development'),
        ('medical', 'Medical Services'),
        ('miscellaneous', 'Miscellaneous')
    ])

    SERVICE_TYPES = {
        "beauty": ['makeup', 'hair', 'tanning', 'tattoo', 'fashion', 'nail'],
        "health": ['spa', 'gym', 'cardio'],
        "entertainment": ['magic', 'comedy', 'drama', 'music'],
        "sport": ['tennis', 'skating', 'surfing_sailing', 'scuba', 'football', 'soccer', 'baseball'],
        "lessons": [
            'art_lessons', 'music_lessons', 'stem_lessons', 'fitness_lessons',
            'beauty_lessons', 'miscellaneous_lessons'
        ],
        "home": ['interior_decor', 'electrical', 'plumbing', 'landscaping', 'buy_sell_home'],
        "auto": ['cleaning', 'mechanic', 'buy_sell_auto'],
        'personal': ['dating', 'matrimonial', 'personality_dev'],
        'medical': ['dentist', 'nurse', 'doctor', 'acupuncture', 'chiropractor', 'physio']
    }

    TYPE = OrderedDict([
        ('makeup', 'Makeup Studio'),
        ('hair', 'Hair Studio'),
        ('tanning', 'Tanning Services'),
        ('tattoo', 'Tattoo & Piercings'),
        ('fashion', 'Fashion Services'),
        ('nail', 'Nail Salon'),

        ('spa', 'Massage & Spa Salon'),
        ('gym', 'Gym, Strength & Crossfit'),
        ('cardio', 'Zumba, Yoga, Pilates, Aerobics'),

        ('magic', 'Magic, Hypnotism & Illusions'),
        ('comedy', 'Comedy Shows'),
        ('drama', 'Drama'),
        ('music', 'DJ, Music & Orchestra'),

        ('tennis', 'Tennis Training'),
        ('skating', 'Skating & Skiing'),
        ('surfing_sailing', 'Surfing & Sailing'),
        ('scuba', 'Diving, Snorkel & Scuba'),
        ('football', 'American Football'),
        ('soccer', 'Soccer Training'),
        ('baseball', 'Baseball Training'),

        ('art_lessons', 'Design, Animation, Graphics Lessons'),
        ('music_lessons', 'Music Lessons'),
        ('stem_lessons', 'Science, Tech, Engineering & Math Lessons'),
        ('fitness_lessons', 'Fitness & Health Lessons'),
        ('beauty_lessons', 'Beauty Lessons'),
        ('miscellaneous_lessons', 'Other Lessons & Training'),

        ('interior_decor', 'Home Interior Decor'),
        ('electrical', 'Electrical'),
        ('plumbing', 'Plumbing'),
        ('landscaping', 'Landscaping'),
        ('buy_sell_home', 'Buy/Sell Home, Financing'),

        ('cleaning', 'Auto Cleaning & Detailing'),
        ('mechanic', 'Auto Mechanic'),
        ('buy_sell_auto', 'Buy/Sell Auto, Financing'),

        ('dating', 'Dating Services'),
        ('matrimonial', 'Matrimonial Services'),
        ('personality_dev', 'Personality Development - Speaking, Mannerisma'),

        ('dentist', 'Dental Services'),
        ('nurse', 'Nurse'),
        ('doctor', 'Doctor'),
        ('acupuncture', 'Acu-Puncture'),
        ('chiropractor', 'Chiropractic Services'),
        ('physio', 'Physiotherapy')
    ])

    TYPE_IMAGE_DIR = OrderedDict([
        ('makeup', 'dashboard/global/img/portfolio/Beauty/Makeup'),
        ('hair', 'dashboard/global/img/portfolio/Beauty/Hair'),
        ('tanning', 'dashboard/global/img/portfolio/Beauty/Tanning'),
        ('tattoo', 'dashboard/global/img/portfolio/Beauty/Tattoo'),
        ('fashion', 'dashboard/global/img/portfolio/Beauty/Fashion'),
        ('nail', 'dashboard/global/img/portfolio/Beauty/Nail'),

        ('spa', 'dashboard/global/img/portfolio/Health/Spa'),
        ('gym', 'dashboard/global/img/portfolio/Health/Gym'),
        ('cardio', 'dashboard/global/img/portfolio/Health/Cardio'),

        ('magic', 'dashboard/global/img/portfolio/test'),
        ('comedy', 'dashboard/global/img/portfolio/test'),
        ('drama', 'dashboard/global/img/portfolio/test'),
        ('music', 'dashboard/global/img/portfolio/test'),

        ('tennis', 'dashboard/global/img/portfolio/test'),
        ('skating', 'dashboard/global/img/portfolio/test'),
        ('surfing_sailing', 'dashboard/global/img/portfolio/test'),
        ('scuba', 'dashboard/global/img/portfolio/test'),
        ('football', 'dashboard/global/img/portfolio'),
        ('soccer', 'dashboard/global/img/portfolio/test'),
        ('baseball', 'dashboard/global/img/portfolio/test'),

        ('art_lessons', 'dashboard/global/img/portfolio/test'),
        ('music_lessons', 'dashboard/global/img/portfolio/test'),
        ('stem_lessons', 'dashboard/global/img/portfolio/test'),
        ('fitness_lessons', 'dashboard/global/img/portfolio/test'),
        ('beauty_lessons', 'dashboard/global/img/portfolio/test'),
        ('miscellaneous_lessons', 'dashboard/global/img/portfolio/test'),

        ('interior_decor', 'dashboard/global/img/portfolio/test'),
        ('electrical', 'dashboard/global/img/portfolio/test'),
        ('plumbing', 'dashboard/global/img/portfolio/test'),
        ('landscaping', 'dashboard/global/img/portfolio/test'),
        ('buy_sell_home', 'dashboard/global/img/portfolio/test'),

        ('cleaning', 'dashboard/global/img/portfolio/test'),
        ('mechanic', 'dashboard/global/img/portfolio/test'),
        ('buy_sell_auto', 'dashboard/global/img/portfolio/test'),

        ('dating', 'dashboard/global/img/portfolio/test'),
        ('matrimonial', 'dashboard/global/img/portfolio/test'),
        ('personality_dev', 'dashboard/global/img/portfolio/test'),

        ('dentist', 'dashboard/global/img/portfolio/test'),
        ('nurse', 'dashboard/global/img/portfolio/test'),
        ('doctor', 'dashboard/global/img/portfolio/test'),
        ('acupuncture', 'dashboard/global/img/portfolio/test'),
        ('chiropractor', 'dashboard/global/img/portfolio/test'),
        ('physio', 'dashboard/global/img/portfolio/test')
    ])

    METRO = OrderedDict([
        ('sf', 'SF Bay Area'),
        ('ny', 'New York'),
        ('chicago', 'Chicago'),
        ('boston', 'Boston'),
        ('atlanta', 'Atlanta'),
        ('la', 'Los Angeles'),
        ('sd', 'San Diego'),
        ('miami', 'Miami'),
        ('other', 'Other')
    ])

    # Details
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), index=True)
    type = db.Column(db.Enum(*TYPE, name='business_types'), index=True, nullable=False, server_default=TYPE.keys()[0])
    about = db.Column(db.Text())

    opening_time = db.Column(db.Time())
    closing_time = db.Column(db.Time())
    weekends_open = db.Column('is_open_weekends', db.Boolean(), server_default='0')

    phone = db.Column(db.String(20), index=True)
    website = db.Column(db.String(32))
    twitter = db.Column(db.String(64))
    facebook = db.Column(db.String(64))
    youtube = db.Column(db.String(64))
    linkedin = db.Column(db.String(64))
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
    points = db.Column(db.Integer, nullable=False, server_default='0')

    # Relationships.
    # Many to One relationship: Many users can have same address
    # http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'))
    address = db.relationship(Address)
    metro = db.Column(db.Enum(*METRO, name='metro'), index=True, nullable=False, server_default="other")

    # One to Many relationship: One business can have multiple occupancies
    occupancies = db.relationship(Occupancy, backref="business")
    products = db.relationship(Product, backref='business', passive_deletes=True)
    employees = db.relationship(Employee, backref='business', passive_deletes=True)
    customers = db.relationship(Customer, backref='business', passive_deletes=True)
    reservations = db.relationship(Reservation, backref='business', passive_deletes=True)
    reviews = db.relationship(Review, backref='business', passive_deletes=True)


    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(Business, self).__init__(**kwargs)

    @classmethod
    def search(cls, query):
        """
        Search a resource by 1 or more fields.

        :param query: Search query
        :type query: str
        :return: SQLAlchemy filter
        """
        if not query:
            return ''

        search_query = '%{0}%'.format(query)
        search_chain = (cls.email.ilike(search_query),
                        cls.name.ilike(search_query))

        return or_(*search_chain)

    @classmethod
    def create_from_form(cls, form):
        """
        Return whether or not the business was created successfully.

        :return: bool
        """

        business = cls()
        form.populate_obj(business)

        # Create Business Address
        business.address = Address()
        form.populate_obj(business.address)

        business = business.save()

        # Create the first Admin employee for this newly created business
        admin_employee_params = {
            'name': current_user.name,
            'email': current_user.email
        }
        Employee.get_or_create(business_id=business.id, **admin_employee_params)

        return True

    def modify_from_form(self, form):
        """
        Return whether or not the business was modified successfully.

        :return: bool
        """

        form.populate_obj(self)
        # Create Business Address if it dint exist previously
        if not self.address:
            self.address = Address()
        form.populate_obj(self.address)

        self.save()

        return True

    @property
    def active_products(self):
        return list(
                    Product.query.filter(
                        Product.id.in_([product.id for product in self.products]),
                        Product.active
                    )
            )

    @property
    def active_employees(self):
        return list(
                    Employee.query.filter(
                        Employee.id.in_([employee.id for employee in self.employees]),
                        Employee.active
                    )
            )

    @classmethod
    def type_images(cls, type):
        type_images = []
        for img_file in os.listdir(os.path.join(STATIC_FILES_PATH, cls.TYPE_IMAGE_DIR[type])):
            type_images.append(os.path.join(cls.TYPE_IMAGE_DIR[type], img_file))
        return type_images

    @property
    def total_sales(self):
        total_sales_in_cents = sum([item.product.price_cents for item in self.reservations])
        total_sales = total_sales_in_cents/100
        return total_sales

    @property
    def reservation_statuses_count(self):
        statuses = dict()
        for status in Reservation.STATUS.keys():
            statuses[status] = 0

        for reservation in self.reservations:
            statuses[reservation.status] += 1

        return statuses

    @classmethod
    def request_a_review(cls, business_id, customer_id):
        """
        Request a review
        """
        from lyfeshoppe.blueprints.business.tasks import request_customer_review
        request_customer_review.delay(business_id, customer_id)
