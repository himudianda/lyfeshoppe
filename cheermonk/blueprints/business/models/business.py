from collections import OrderedDict
from sqlalchemy import or_

from cheermonk.lib.util_sqlalchemy import ResourceMixin, AwareDateTime
from cheermonk.blueprints.common.models import Address, Occupancy, Availability
from cheermonk.extensions import db


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

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(Product, self).__init__(**kwargs)


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
