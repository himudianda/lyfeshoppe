from cheermonk.lib.util_sqlalchemy import AwareDateTime
from cheermonk.extensions import db


class Occupancy(db.Model):
    __tablename__ = 'occupancies'

    # Details
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(AwareDateTime())
    end_time = db.Column(AwareDateTime())
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')


class Availability(db.Model):
    __tablename__ = 'availabilities'

    # Details
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(AwareDateTime())
    end_time = db.Column(AwareDateTime())
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')


class Address(db.Model):
    __tablename__ = 'addresses'

    # Details
    id = db.Column(db.Integer, primary_key=True)

    street = db.Column(db.String(128))
    city = db.Column(db.String(20))
    state = db.Column(db.String(20))
    zipcode = db.Column(db.String(10))
