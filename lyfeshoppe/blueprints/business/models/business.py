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
        ('new', 'New reservation'),
        ('processing', 'Reservation being currently processed'),
        ('confirmed', 'Reservation Confirmed'),
        ('cancelled', 'Reservation Cancelled'),
        ('executed', 'Product/Service was provided')
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

        reservation = cls(**params)

        db.session.add(reservation)
        db.session.commit()

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
    def create(cls, params):
        """
        Return whether or not the employee was created successfully.

        :return: bool
        """
        employee = cls(**params)
        db.session.add(employee)
        db.session.commit()

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
    def create(cls, params):
        """
        Return whether or not the product was created successfully.

        :return: bool
        """
        product = cls(**params)
        db.session.add(product)
        db.session.commit()

        return True


class Business(ResourceMixin, db.Model):
    __tablename__ = 'businesses'

    TYPE = OrderedDict([
        ('acupuncture', 'Acupuncture'),
        ('barber', 'Barber'),
        ('massage', 'Massage'),
        ('makeup', 'Makeup'),
        ('pets_salon', 'Pets Salon'),
        ('spa', 'Spa'),
        ('tattoo', 'Tattoo'),
        ('tanning', 'Tanning'),
        ('photo_studio', 'Photo Studio')
    ])

    BUSINESS_TYPE_IMAGES = OrderedDict([
        ('acupuncture', 'dashboard/global/img/portfolio/600x600/013.jpg'),
        ('barber', 'dashboard/global/img/portfolio/600x600/05.jpg'),
        ('massage', 'dashboard/global/img/portfolio/600x600/16.jpg'),
        ('makeup', 'dashboard/global/img/portfolio/600x600/33.jpg'),
        ('pets_salon', 'dashboard/global/img/portfolio/600x600/38.jpg'),
        ('spa', 'dashboard/global/img/portfolio/600x600/88.jpg'),
        ('tattoo', 'dashboard/global/img/portfolio/600x600/02.jpg'),
        ('tanning', 'dashboard/global/img/portfolio/600x600/62.jpg'),
        ('photo_studio', 'dashboard/global/img/portfolio/600x600/81.jpg')
    ])

    # Details
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), index=True)
    type = db.Column(db.Enum(*TYPE, name='business_types'), index=True, nullable=False, server_default='massage')

    open_time = db.Column(AwareDateTime())
    close_time = db.Column(AwareDateTime())
    phone = db.Column(db.String(20), index=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    # Relationships.
    # Many to One relationship: Many users can have same address
    # http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'))
    address = db.relationship(Address)
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
    def create(cls, params):
        """
        Return whether or not the business was created successfully.

        :return: bool
        """

        if 'open_time' in params:
            if params.get('open_time') is not None:
                params['open_time'] = params.get('open_time').replace(
                    tzinfo=pytz.UTC)

        if 'close_time' in params:
            if params.get('close_time') is not None:
                params['close_time'] = params.get('close_time').replace(
                    tzinfo=pytz.UTC)

        business = Business(**params)

        db.session.add(business)
        db.session.commit()

        # Create the first Admin employee for this newly created business
        admin_employee_params = {
            'role': 'admin',
            'user_id': current_user.id,
            'business_id': business.id,
            'user': current_user
        }
        Employee.create(admin_employee_params)

        return True
