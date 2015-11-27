from cheermonk.lib.util_sqlalchemy import ResourceMixin
from cheermonk.extensions import db


class Product(ResourceMixin, db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)

    # Relationships.
    business_id = db.Column(db.Integer, db.ForeignKey('businesses.id',
                                                      onupdate='CASCADE',
                                                      ondelete='CASCADE'),
                            index=True, nullable=False)

    # Product Details.
    title = db.Column(db.String(128))
    description = db.Column(db.Text())
    price = db.Column(db.Integer())
