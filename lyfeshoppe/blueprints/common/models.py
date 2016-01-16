from lyfeshoppe.extensions import db


class Address(db.Model):
    __tablename__ = 'addresses'

    # Details
    id = db.Column(db.Integer, primary_key=True)

    street = db.Column(db.String(256))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    zipcode = db.Column(db.String(20))
    district = db.Column(db.String(100))  # or county name
    country = db.Column(db.String(100))
