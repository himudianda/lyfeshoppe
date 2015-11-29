from cheermonk.lib.util_sqlalchemy import ResourceMixin
from cheermonk.extensions import db


class Business(ResourceMixin, db.Model):
    __tablename__ = 'businesses'
    id = db.Column(db.Integer, primary_key=True)

    # Relationships.
    user_id = db.Column(
                db.Integer,
                db.ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'),
                index=True, nullable=False
            )
    name = db.Column(db.String(128))
    email = db.Column(db.String(255), unique=True, index=True, nullable=False, server_default='')

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(Business, self).__init__(**kwargs)
