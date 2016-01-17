import logging
from collections import OrderedDict
from lyfeshoppe.lib.util_wtforms import ModelForm
from flask_wtf import Form
from wtforms import HiddenField, SelectField, StringField, DateTimeField, BooleanField, TextAreaField
from wtforms_components import EmailField, IntegerField
from wtforms.validators import DataRequired, Length, Optional, NumberRange
from flask_babel import lazy_gettext as _
from lyfeshoppe.blueprints.business.models.business import Business, Reservation, Review

try:
    from instance import settings

    LANGUAGES = settings.LANGUAGES
except ImportError:
    logging.error('Ensure __init__.py and settings.py both exist in instance/')
    exit(1)
except AttributeError:
    from config import settings

    LANGUAGES = settings.LANGUAGES

from lyfeshoppe.lib.util_wtforms import choices_from_dict
from lyfeshoppe.lib.field_widgets import DateTimePickerWidget


class SearchForm(Form):
    q = StringField(_('Search terms'), [Optional(), Length(1, 128)])


class BulkDeleteForm(Form):
    SCOPE = OrderedDict([
        ('all_selected_products', 'All selected items'),
        ('all_search_results', 'All search results')
    ])

    scope = SelectField(_('Privileges'), [DataRequired()],
                        choices=choices_from_dict(SCOPE, prepend_blank=False))


class WelcomeForm(ModelForm):
    country = StringField(_('Country'), [DataRequired()])
    state = StringField(_('State/Province'), [DataRequired()])
    city = StringField(_('City/Town'), [DataRequired()])
    zipcode = StringField(_('Zip/Post Code'), [Optional(), Length(1, 30)])
    metro = SelectField(_('Metro Area'), [DataRequired()],
                        choices=choices_from_dict(Business.METRO, prepend_blank=False))
    phone = StringField(_('Phone number'), [Optional(), Length(1, 12)])
    gender = SelectField(_('Gender'), [DataRequired()], choices=(('male', "Male"), ('female', "Female")))


class UserAccountForm(ModelForm):

    first_name = StringField(_('First Name'), [DataRequired(), Length(1, 255)])
    last_name = StringField(_('Last Name'), [DataRequired(), Length(1, 255)])
    email = EmailField(_("Email Address"),
                       [DataRequired(), Length(3, 254)])
    phone = StringField(_('Phone number'), [Optional(), Length(1, 12)])
    street = StringField(_('Full Street Address'), [Optional(), Length(1, 255)])
    city = StringField(_('City'), [Optional(), Length(1, 30)])
    state = StringField(_('State'), [Optional(), Length(1, 30)])
    zipcode = StringField(_('Zipcode'), [Optional(), Length(1, 30)])
    district = StringField(_('District/County'), [Optional(), Length(1, 30)])
    country = StringField(_('Country'), [Optional(), Length(1, 30)])


class BusinessForm(ModelForm):

    name = StringField(_('Business name'), [DataRequired(), Length(1, 255)])
    email = EmailField(_("Email Address"), [DataRequired(), Length(3, 255)])
    type = SelectField(_('Business Type'), [DataRequired()],
                       choices=choices_from_dict(Business.TYPE, prepend_blank=False))
    about = TextAreaField(_("About the Business"), [Optional(), Length(3, 2048)])
    opening_time = StringField(_('Opening time'), [DataRequired()], widget=DateTimePickerWidget())
    closing_time = StringField(_('Closing time'), [DataRequired()], widget=DateTimePickerWidget())
    weekends_open = BooleanField(_('Yes, Open on weekends'))

    phone = StringField(_('Business Phone number'), [DataRequired(), Length(1, 12)])
    website = StringField(_('Website'), [Optional(), Length(0, 32)])
    twitter = StringField(_('Twitter Profile'), [Optional(), Length(0, 64)])
    facebook = StringField(_('Facebook Profile'), [Optional(), Length(0, 64)])
    youtube = StringField(_('Youtube Profile'), [Optional(), Length(0, 64)])
    linkedin = StringField(_('LinkedIn Profile'), [Optional(), Length(0, 64)])

    active = BooleanField(_('Yes, Business is active'))

    metro = SelectField(_('Metro'), [DataRequired()],
                        choices=choices_from_dict(Business.METRO, prepend_blank=False))
    street = StringField(_('Street Address'), [DataRequired(), Length(1, 255)])
    city = StringField(_('City'), [DataRequired(), Length(1, 30)])
    state = StringField(_('State'), [DataRequired(), Length(1, 30)])
    zipcode = StringField(_('Zipcode'), [DataRequired(), Length(1, 30)])
    district = StringField(_('District/County'), [Optional(), Length(1, 30)])
    country = StringField(_('Country'), [DataRequired(), Length(1, 30)])


class EmployeeForm(ModelForm):
    first_name = StringField(_('First Name'), [DataRequired(), Length(1, 255)])
    last_name = StringField(_('Last Name'), [DataRequired(), Length(1, 255)])
    email = EmailField(_("Email Address"),
                       [DataRequired(), Length(3, 254)])
    phone = StringField(_('Phone number'), [Optional(), Length(1, 12)])
    about = TextAreaField(_("About the Employee"), [Optional(), Length(3, 2048)])
    street = StringField(_('Full Street Address'), [Optional(), Length(1, 255)])
    city = StringField(_('City'), [Optional(), Length(1, 30)])
    state = StringField(_('State'), [Optional(), Length(1, 30)])
    zipcode = StringField(_('Zipcode'), [Optional(), Length(1, 30)])
    district = StringField(_('District/County'), [Optional(), Length(1, 30)])
    country = StringField(_('Country'), [Optional(), Length(1, 30)])
    active = BooleanField(_('Yes, Employee is active'))


class CustomerForm(ModelForm):
    first_name = StringField(_('First Name'), [DataRequired(), Length(1, 255)])
    last_name = StringField(_('Last Name'), [DataRequired(), Length(1, 255)])
    email = EmailField(_("Email Address"),
                       [DataRequired(), Length(3, 254)])
    phone = StringField(_('Phone number'), [Optional(), Length(1, 12)])
    street = StringField(_('Full Street Address'), [Optional(), Length(1, 255)])
    city = StringField(_('City'), [Optional(), Length(1, 30)])
    state = StringField(_('State'), [Optional(), Length(1, 30)])
    zipcode = StringField(_('Zipcode'), [Optional(), Length(1, 30)])
    district = StringField(_('District/County'), [Optional(), Length(1, 30)])
    country = StringField(_('Country'), [Optional(), Length(1, 30)])
    active = BooleanField(_('Yes, Employee is active'))


class ProductForm(ModelForm):

    name = StringField(_('Product name'), [DataRequired(), Length(1, 128)])
    category = StringField(_('Product Category'), [DataRequired(), Length(1, 32)])
    description = TextAreaField(_("Product description"), [DataRequired(), Length(3, 2048)])
    capacity = IntegerField(_('Service Capacity'), [Optional(), NumberRange(min=1, max=1000)])
    price_cents = IntegerField(_('Price in cents'), [Optional(), NumberRange(min=1, max=1000000)])
    duration_mins = IntegerField(_('Duration in mins'), [Optional(), NumberRange(min=1, max=1000)])

    active = BooleanField(_('Yes, Product is active'))


class ReservationForm(ModelForm):
    employee_id = HiddenField()
    product_id = HiddenField()
    customer_email = EmailField(_("Email Address"), [DataRequired(), Length(3, 254)])
    start_time = DateTimeField(_('Start time'), [Optional()], format='%Y-%m-%d %H:%M:%S')
    end_time = DateTimeField(_('End time'), [Optional()], format='%Y-%m-%d %H:%M:%S')


class ReservationEditForm(ModelForm):
    reservation_id = HiddenField()
    status = SelectField(_('Reservation Status'), [DataRequired()],
                         choices=choices_from_dict(Reservation.STATUS,
                         prepend_blank=False))


class BookingForm(ModelForm):
    employee_id = HiddenField()
    start_time = DateTimeField(_('Start time'), [Optional()], format='%Y-%m-%d %H:%M:%S')
    end_time = DateTimeField(_('End time'), [Optional()], format='%Y-%m-%d %H:%M:%S')


class ReviewForm(ModelForm):
    product_id = HiddenField()
    status = SelectField(_('Status'), [DataRequired()],
                         choices=choices_from_dict(Review.STATUS,
                         prepend_blank=False))
    description = TextAreaField(_("description"), [DataRequired(), Length(3, 2048)])


class ReferralForm(Form):
    first_name_1 = StringField(_('First Name'), [DataRequired(), Length(1, 128)])
    last_name_1 = StringField(_('Last Name'), [DataRequired(), Length(1, 128)])
    email_1 = EmailField(_("Email Address"), [DataRequired(), Length(3, 254)])
    gender_1 = SelectField(_('Gender'), [DataRequired()], choices=[('male', 'Male'), ('female', 'Female')])

    first_name_2 = StringField(_('First Name'), [DataRequired(), Length(1, 128)])
    last_name_2 = StringField(_('Last Name'), [DataRequired(), Length(1, 128)])
    email_2 = EmailField(_("Email Address"), [DataRequired(), Length(3, 254)])
    gender_2 = SelectField(_('Gender'), [DataRequired()], choices=[('male', 'Male'), ('female', 'Female')])

    first_name_3 = StringField(_('First Name'), [DataRequired(), Length(1, 128)])
    last_name_3 = StringField(_('Last Name'), [DataRequired(), Length(1, 128)])
    email_3 = EmailField(_("Email Address"), [DataRequired(), Length(3, 254)])
    gender_3 = SelectField(_('Gender'), [DataRequired()], choices=[('male', 'Male'), ('female', 'Female')])
