from collections import OrderedDict

from lyfeshoppe.lib.util_sqlalchemy import AwareDateTime
from lyfeshoppe.extensions import db


class Occupancy(db.Model):
    __tablename__ = 'occupancies'

    TYPE = OrderedDict([
        ('user', 'User Occupancy Record'),
        ('business', 'Business Occupancy Record')
    ])

    # Details
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum(*TYPE, name='occupancy_types'), index=True, nullable=False, server_default='user')
    start_time = db.Column(AwareDateTime())
    end_time = db.Column(AwareDateTime())
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    business_id = db.Column(db.Integer, db.ForeignKey('businesses.id'))


class Availability(db.Model):
    __tablename__ = 'availabilities'

    TYPE = OrderedDict([
        ('product', 'Product Occupancy Record')
    ])

    # Details
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum(*TYPE, name='availability_types'), index=True, nullable=False, server_default='product')
    start_time = db.Column(AwareDateTime())
    end_time = db.Column(AwareDateTime())
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    # Relationships
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))


class Address(db.Model):
    __tablename__ = 'addresses'

    # Details
    id = db.Column(db.Integer, primary_key=True)

    street = db.Column(db.String(256))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    zipcode = db.Column(db.String(20))
    district = db.Column(db.String(50))  # or county name
    country = db.Column(db.String(50))
