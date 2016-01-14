import datetime
from collections import OrderedDict
from hashlib import md5
import random
import string
import pytz
from flask import current_app

from flask_login import UserMixin

from itsdangerous import URLSafeTimedSerializer, \
    TimedJSONWebSignatureSerializer

from sqlalchemy import or_

from lyfeshoppe.lib.util_sqlalchemy import ResourceMixin, AwareDateTime
from lyfeshoppe.blueprints.common.models import Address, Occupancy
from lyfeshoppe.blueprints.billing.models.credit_card import CreditCard
from lyfeshoppe.blueprints.billing.models.subscription import Subscription
from lyfeshoppe.blueprints.billing.models.invoice import Invoice
from lyfeshoppe.extensions import db, bcrypt


class Referral(ResourceMixin, db.Model):
    __tablename__ = 'referrals'

    STATUS = OrderedDict([
        ('pending', 'Pending'),
        ('accepted', 'Accepted')
    ])

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum(*STATUS, name='referral_status'), index=True, nullable=False, server_default='pending')

    # 2 foreign keys to the same table
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    user = db.relationship("User", foreign_keys=[user_id])
    reference_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    reference = db.relationship("User", foreign_keys=[reference_id])

    @classmethod
    def create(cls, user_id, reference_email, reference_name):
        """
        Create a referral instance.

        :return: self
        """
        user = User.query.get(user_id)
        if not user:
            return None, "System Error: user_id cannot be found"

        ref_user = User.find_by_identity(reference_email)
        if ref_user:
            return None, "{0} already exists. Referral cannot be created".format(reference_email)

        ref_user = User(email=reference_email, name=reference_name, password="password")
        ref_user.save()
        referral = cls(user_id=user_id, reference_id=ref_user.id)
        referral.save()
        return referral, "Referral for {0} was successfully created".format(reference_email)


class User(UserMixin, ResourceMixin, db.Model):
    __tablename__ = 'users'

    ROLE = OrderedDict([
        ('member', 'Member'),
        ('admin', 'Admin')
    ])

    id = db.Column(db.Integer, primary_key=True)

    # Details
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    name = db.Column(db.String(128), index=True)
    phone = db.Column(db.String(20), index=True)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False, server_default='')

    social_id = db.Column(db.String(64), unique=True)
    fb_id = db.Column(db.String(64), unique=True)
    fb_link = db.Column(db.String(128), unique=True)
    fb_verified = db.Column('is_fb_verified', db.Boolean(), nullable=False, server_default='0')
    fb_added = db.Column('is_fb_added', db.Boolean(), nullable=False, server_default='0')
    first_name = db.Column(db.String(128), index=True)
    last_name = db.Column(db.String(128), index=True)
    age_range_min = db.Column(db.Integer)
    age_range_max = db.Column(db.Integer)
    gender = db.Column(db.String(32))
    timezone = db.Column(db.Integer)

    # Authentication.
    role = db.Column(db.Enum(*ROLE, name='role_types'), index=True, nullable=False, server_default='member')
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    password = db.Column(db.String(128), nullable=False, server_default='')

    # Relationships.
    # Many to One relationship: Many users can have same address
    # http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'))
    address = db.relationship(Address)
    # One to Many relationship: One user can have multiple occupancies
    occupancies = db.relationship(Occupancy, backref="user")
    employee_refs = db.relationship('Employee', backref='user', passive_deletes=True)

    # Locale.
    locale = db.Column(db.String(5), nullable=False, server_default='en')

    credit_card = db.relationship(CreditCard, uselist=False, backref='users', passive_deletes=True)
    subscription = db.relationship(Subscription, uselist=False, backref='users', passive_deletes=True)
    invoices = db.relationship(Invoice, backref='users', passive_deletes=True)

    # Billing.
    payment_id = db.Column(db.String(128), index=True)
    cancelled_subscription_on = db.Column(AwareDateTime())

    # Activity tracking.
    sign_in_count = db.Column(db.Integer, nullable=False, default=0)
    current_sign_in_on = db.Column(AwareDateTime())
    current_sign_in_ip = db.Column(db.String(45))
    last_sign_in_on = db.Column(AwareDateTime())
    last_sign_in_ip = db.Column(db.String(45))

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(User, self).__init__(**kwargs)

        self.password = User.encrypt_password(kwargs.get('password', ''))
        if kwargs.get('email', None) and not self.username:
            self.username = kwargs.get('email').split('@')[0]

    def save(self):
        """
        Save a model instance.

        :return: self
        """
        if not self.username:
            username = self.email.split('@')[0]

            user = User.find_by_identity(username)
            count = 0
            while user:
                count += 1
                username = username + str(count)
                user = User.find_by_identity(username)

            self.username = username

        return super(User, self).save()

    @classmethod
    def get_or_create(cls, params=None, from_form=False, form=None):
        """
        Return whether or not the user was created successfully.

        :return: bool
        """

        if from_form:
            new_user = cls()
            form.populate_obj(new_user)
            customer_email = new_user.email
        else:
            if 'email' in params:
                customer_email = params.get('email', None)

        user = User.find_by_identity(customer_email)
        if not user:
            if from_form:
                user = cls()
                form.populate_obj(user)

                # Create Business Address
                user.address = Address()
                form.populate_obj(user.address)
            else:
                user = cls(**params)

            # Generate a random password
            pwd_size = 8
            chars = string.ascii_uppercase + string.digits
            pwd = ''.join(random.choice(chars) for _ in range(pwd_size))
            user.password = pwd
            user = user.save()

            # This prevents circular imports.
            from lyfeshoppe.blueprints.user.tasks import deliver_new_user_email
            deliver_new_user_email.delay(user.id, pwd)

        return user

    def modify_from_form(self, form):
        """
        Return whether or not the user was modified successfully.

        :return: bool
        """

        form.populate_obj(self)
        # Create User Address if it dint exist previously
        if not self.address:
            self.address = Address()
        form.populate_obj(self.address)

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
        search_chain = (cls.email.ilike(search_query),
                        cls.name.ilike(search_query))

        return or_(*search_chain)

    @classmethod
    def find_by_identity(cls, identity):
        """
        Find a user by their e-mail or username.

        :param identity: Email or username
        :type identity: str
        :return: User instance
        """
        return cls.query.filter((cls.email == identity) | (cls.username == identity)).first()

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
        Obtain a user from de-serializing a signed token.

        :param token: Signed token.
        :type token: str
        :return: User instance or None
        """
        private_key = TimedJSONWebSignatureSerializer(
            current_app.config['SECRET_KEY'])
        try:
            decoded_payload = private_key.loads(token)

            return cls.find_by_identity(decoded_payload.get('user_email'))
        except Exception:
            return None

    @classmethod
    def initialize_password_reset(cls, identity):
        """
        Generate a token to reset the password for a specific user.

        :param identity: User e-mail address or username
        :type identity: str
        :return: User instance
        """
        u = cls.find_by_identity(identity)
        reset_token = u.serialize_token()

        # This prevents circular imports.
        from lyfeshoppe.blueprints.user.tasks import deliver_password_reset_email

        deliver_password_reset_email.delay(u.id, reset_token)

        return u

    def is_active(self):
        """
        Return whether or not the user account is active, this satisfies
        Flask-Login by overwriting the default value.

        :return: bool
        """
        return self.active

    def get_auth_token(self):
        """
        Return the user's auth token. Use their password as part of the token
        because if the user changes their password we will want to invalidate
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
        Ensure a user is authenticated, and optionally check their password.

        :param with_password: Optionally check their password
        :type with_password: bool
        :param password: Optionally verify this as their password
        :type password: str
        :return: bool
        """
        if with_password:
            if not self.password:
                return False
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

    def update_activity_tracking(self, ip_address):
        """
        Update various fields on the user that's related to meta data on his
        account, such as the sign in count and ip address, etc..

        :param ip_address: IP address
        :type ip_address: str
        :return: SQLAlchemy commit results
        """
        self.sign_in_count += 1

        self.last_sign_in_on = self.current_sign_in_on
        self.last_sign_in_ip = self.current_sign_in_ip

        self.current_sign_in_on = datetime.datetime.now(pytz.utc)
        self.current_sign_in_ip = ip_address

        return self.save()

    @classmethod
    def is_last_admin(cls, user, new_role, new_active):
        """
        Determine whether or not this user is the last admin account.

        :param user: User being tested
        :type user: User
        :param new_role: New role being set
        :type new_role: str
        :param new_active: New active status being set
        :type new_active: bool
        :return: bool
        """
        is_changing_roles = user.role == 'admin' and new_role != 'admin'
        is_changing_active = user.active is True and new_active is None

        if is_changing_roles or is_changing_active:
            admin_count = User.query.filter(User.role == 'admin').count()
            active_count = User.query.filter(User.is_active is True).count()

            if admin_count == 1 or active_count == 1:
                return True

        return False

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
            user = User.query.get(id)

            if user is None:
                continue

            if user.payment_id is None:
                user.delete()
            else:
                subscription = Subscription()
                cancelled = subscription.cancel(user=user)

                # If successful, delete it locally.
                if cancelled:
                    user.delete()

            delete_count += 1

        return delete_count

    @property
    def num_of_businesses(self):
        employee_ids = [employee.id for employee in self.employee_refs]
        from lyfeshoppe.blueprints.business.models.business import Business, Employee
        return Business.query.filter(
                                Business.employees.any(Employee.id.in_(employee_ids))
                              ).count()

    @property
    def id_of_businesses(self):
        employee_ids = [employee.id for employee in self.employee_refs]
        from lyfeshoppe.blueprints.business.models.business import Business, Employee
        query = db.session.query(
                                Business.id.distinct().label("id")
                            ).filter(
                                Business.employees.any(Employee.id.in_(employee_ids))
                            )
        ids = [row.id for row in query.all()]
        return ids

    def update_from_facebook_data(
            self, social_id, fb_id, fb_link, fb_verified,
            fb_added, first_name, last_name, locale,
            age_range_min, age_range_max, gender,
            timezone, name, email):
        self.social_id = social_id
        self.fb_id = fb_id
        self.fb_link = fb_link
        self.fb_verified = fb_verified
        self.fb_added = False
        self.first_name = first_name
        self.last_name = last_name
        self.locale = locale
        self.age_range_min = age_range_min
        self.age_range_max = age_range_max
        self.gender = gender
        self.timezone = timezone
        self.name = name

        self.save()
        return self
