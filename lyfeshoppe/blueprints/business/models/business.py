from collections import OrderedDict
from sqlalchemy import or_, UniqueConstraint
import pytz
from flask_login import current_user

from lyfeshoppe.lib.util_sqlalchemy import ResourceMixin, AwareDateTime
from lyfeshoppe.blueprints.common.models import Address, Occupancy, Availability
from lyfeshoppe.blueprints.user.models import User
from lyfeshoppe.extensions import db


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


class Customer(ResourceMixin, db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)

    # Relationships.
    business_id = db.Column(db.Integer, db.ForeignKey(
                        'businesses.id', onupdate='CASCADE', ondelete='CASCADE'
                    ), index=True, nullable=False)

    # Many to One relationship: Many customers can have same user
    # Thats becoz; A customer can belong with multiple businesses.
    # http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship(User)
    reservations = db.relationship(Reservation, backref='customer', passive_deletes=True)

    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    __table_args__ = (UniqueConstraint('user_id', 'business_id', name='_customer_user_business_uc'), )

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(Customer, self).__init__(**kwargs)

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
    def get_or_create_from_form(cls, business_id, form):
        """
        Return whether or not the customer was created successfully.

        :return: bool
        """
        new_customer = cls()
        form.populate_obj(new_customer)

        user = User.find_by_identity(new_customer.email)
        customer = Customer.query.filter(
                        Customer.user == user, Customer.business_id == business_id
                    ).first()
        if customer:
            return (customer, False)  # Customer exists & wasnt created

        customer = cls()
        form.populate_obj(customer)
        customer.business_id = business_id
        customer.user = User.get_or_create(params=None, from_form=True, form=form)

        customer = customer.save()
        return (customer, True)  # New customer was created

    @classmethod
    def get_or_create(cls, business_id, customer_email):
        user = User.find_by_identity(customer_email)
        if not user:
            user = User.get_or_create(params={"email": customer_email})

        customers = cls.query.filter(cls.business_id == business_id)
        for customer in customers:
            if customer.user.email == customer_email:
                return customer

        customer_params = {
            "business_id": business_id,
            "user_id": user.id
        }
        customer = Customer(**customer_params)
        return customer.save()

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


class Employee(ResourceMixin, db.Model):
    __tablename__ = 'employees'

    ROLE = OrderedDict([
        ('admin', 'Admin'),  # Admin employees have full access to Business backends
        ('member', 'Member')  # Member employees only have access to products in a Business that they offer
    ])

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Enum(*ROLE, name='employee_roles'), index=True, nullable=False, server_default='member')

    # Relationships.
    # Many to One relationship: Many employees can have same user
    # Thats becoz; A user can be employed with multiple businesses.
    # http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html
    business_id = db.Column(db.Integer, db.ForeignKey(
                        'businesses.id', onupdate='CASCADE', ondelete='CASCADE'
                    ), index=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
                        'users.id', onupdate='CASCADE', ondelete='CASCADE'
                        ), index=True, nullable=False)

    products = db.relationship('Product', secondary=employee_product_relations, backref='employees')
    reservations = db.relationship(Reservation, backref='employee', passive_deletes=True)

    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    __table_args__ = (UniqueConstraint('user_id', 'business_id', name='_employee_user_business_uc'), )

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(Employee, self).__init__(**kwargs)

    @classmethod
    def get_or_create(cls, business_id, params=None, from_form=False, form=None):
        """
        Return whether or not the employee was created successfully.

        :return: bool
        """

        if from_form:
            new_employee = cls()
            form.populate_obj(new_employee)
            user = User.find_by_identity(new_employee.email)
        else:
            user = User.query.get(params.get('user_id', None))

        employee = Employee.query.filter(
                        Employee.user == user, Employee.business_id == business_id
                    ).first()
        if employee:
            return (employee, False)  # Employee exists & wasnt created

        if from_form:
            employee = cls()
            form.populate_obj(employee)
            employee.user = User.get_or_create(params=None, from_form=True, form=form)
        else:
            employee = cls(**params)

        employee.business_id = business_id
        employee = employee.save()

        return (employee, True)  # New Employee was created

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

    opening_time = db.Column(db.Time())
    closing_time = db.Column(db.Time())
    weekends_open = db.Column('is_open_weekends', db.Boolean(), server_default='0')

    phone = db.Column(db.String(20), index=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

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

        business.save()

        # Create the first Admin employee for this newly created business
        admin_employee_params = {
            'user_id': current_user.id
        }
        Employee.get_or_create(business_id=business.id, params=admin_employee_params, from_form=False, form=None)

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
