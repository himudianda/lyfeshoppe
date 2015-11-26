from hashlib import md5
from flask import current_app
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer, \
    TimedJSONWebSignatureSerializer
from sqlalchemy import or_

from cheermonk.lib.util_sqlalchemy import ResourceMixin
from cheermonk.extensions import db, bcrypt


class Business(UserMixin, ResourceMixin, db.Model):

    __tablename__ = 'businesses'
    id = db.Column(db.Integer, primary_key=True)

    # Authentication.
    active = db.Column('is_active', db.Boolean(), nullable=False,
                       server_default='1')
    name = db.Column(db.String(128), index=True)
    username = db.Column(db.String(24), unique=True, index=True)
    email = db.Column(db.String(255), unique=True, index=True, nullable=False,
                      server_default='')
    password = db.Column(db.String(128), nullable=False, server_default='')

    # Locale.
    locale = db.Column(db.String(5), nullable=False, server_default='en')

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(Business, self).__init__(**kwargs)

        self.password = Business.encrypt_password(kwargs.get('password', ''))

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
        search_chain = (Business.email.ilike(search_query),
                        Business.name.ilike(search_query))

        return or_(*search_chain)

    @classmethod
    def find_by_identity(cls, identity):
        """
        Find a business by their e-mail or username.

        :param identity: Email or username
        :type identity: str
        :return: Business instance
        """
        return Business.query.filter((Business.email == identity) | (Business.username == identity)).first()

    @classmethod
    def encrypt_password(cls, plaintext_password):
        """
        Hash a plaintext string using bcrypt.

        :param plaintext_password: Password in plain text
        :type plaintext_password: str
        :return: str
        """
        if plaintext_password:
            return bcrypt.generate_password_hash(plaintext_password, 8)

        return None

    @classmethod
    def deserialize_token(cls, token):
        """
        Obtain a business from de-serializing a signed token.

        :param token: Signed token.
        :type token: str
        :return: Business instance or None
        """
        private_key = TimedJSONWebSignatureSerializer(
            current_app.config['SECRET_KEY'])
        try:
            decoded_payload = private_key.loads(token)

            return Business.find_by_identity(decoded_payload.get('user_email'))
        except Exception:
            return None

    @classmethod
    def bulk_delete(cls, ids):
        """
        Override the general bulk_delete method because we need to delete them
        one at a time while also deleting them on Stripe.

        :param ids: List of ids to be deleted
        :type ids: list
        :return: int
        """
        delete_count = 0

        for id in ids:
            business = Business.query.get(id)

            if business is None:
                continue

            business.delete()
            delete_count += 1

        return delete_count

    @classmethod
    def initialize_password_reset(cls, identity):
        """
        Generate a token to reset the password for a specific business.

        :param identity: Business e-mail address or username
        :type identity: str
        :return: Business instance
        """
        u = Business.find_by_identity(identity)
        reset_token = u.serialize_token()

        # This prevents circular imports.
        from cheermonk.blueprints.user.tasks import deliver_password_reset_email

        deliver_password_reset_email.delay(u.id, reset_token)

        return u

    def is_active(self):
        """
        Return whether or not the business account is active, this satisfies
        Flask-Login by overwriting the default value.

        :return: bool
        """
        return self.active

    def get_auth_token(self):
        """
        Return the business's auth token. Use their password as part of the token
        because if the business changes their password we will want to invalidate
        all of their logins across devices. It is completely fine to use
        md5 here as nothing leaks.

        This satisfies Flask-Login by providing a means to create a token.

        :return: str
        """
        private_key = current_app.config['SECRET_KEY']

        serializer = URLSafeTimedSerializer(private_key)
        data = [str(self.id), md5(self.password).hexdigest()]

        return serializer.dumps(data).decode('utf-8')

    def authenticated(self, with_password=True, password=''):
        """
        Ensure a business is authenticated, and optionally check their password.

        :param with_password: Optionally check their password
        :type with_password: bool
        :param password: Optionally verify this as their password
        :type password: str
        :return: bool
        """
        if with_password:
            return bcrypt.check_password_hash(self.password, password)

        return True

    def serialize_token(self, expiration=3600):
        """
        Sign and create a token that can be used for things such as resetting
        a password or other tasks that involve a one off token.

        :param expiration: Seconds until it expires, defaults to 1 hour
        :type expiration: int
        :return: JSON
        """
        private_key = current_app.config['SECRET_KEY']

        serializer = TimedJSONWebSignatureSerializer(private_key, expiration)
        return serializer.dumps({'user_email': self.email}).decode('utf-8')
