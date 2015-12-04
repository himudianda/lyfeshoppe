from collections import OrderedDict
from sqlalchemy import or_

from cheermonk.lib.util_sqlalchemy import ResourceMixin
from cheermonk.extensions import db


class Inventory(ResourceMixin, db.Model):
    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True)

    # Relationships.
    product_id = db.Column(db.Integer, db.ForeignKey(
                        'products.id', onupdate='CASCADE', ondelete='CASCADE'
                    ), index=True, nullable=False)
    price = db.Column(db.Integer, nullable=False, default=0)

    # Example: Massage has count 1
    # Example: Yoga classes & sports training can how count >= 1
    count = db.Column(db.Integer, nullable=False, default=0)


class Product(ResourceMixin, db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(128), nullable=False, server_default='')
    description = db.Column(db.Text())
    price = db.Column(db.Integer, nullable=False, default=0)

    inventory = db.relationship(Inventory, backref='products', passive_deletes=True)

    # Relationships.
    business_id = db.Column(db.Integer, db.ForeignKey(
                        'businesses.id', onupdate='CASCADE', ondelete='CASCADE'
                    ), index=True, nullable=False)

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(Product, self).__init__(**kwargs)


class Business(ResourceMixin, db.Model):
    __tablename__ = 'businesses'
    id = db.Column(db.Integer, primary_key=True)

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
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, index=True, nullable=False, server_default='')
    type = db.Column(db.Enum(*TYPE, name='business_types'), index=True, nullable=False, server_default='massage')

    products = db.relationship(Product, backref='businesses', passive_deletes=True)

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
