import logging
from collections import OrderedDict
from lyfeshoppe.lib.util_wtforms import ModelForm

from flask_wtf import Form
from wtforms import HiddenField, SelectField, StringField, DateTimeField, BooleanField, TextAreaField
from wtforms_components import EmailField, IntegerField, TimeField
from wtforms.validators import DataRequired, Length, Optional, NumberRange
from flask_babel import lazy_gettext as _
from lyfeshoppe.blueprints.business.models.business import Business, Employee, Reservation

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


class SearchForm(Form):
    q = StringField(_('Search terms'), [Optional(), Length(1, 128)])


class BulkDeleteForm(Form):
    SCOPE = OrderedDict([
        ('all_selected_products', 'All selected items'),
        ('all_search_results', 'All search results')
    ])

    scope = SelectField(_('Privileges'), [DataRequired()],
                        choices=choices_from_dict(SCOPE, prepend_blank=False))


class UserAccountForm(ModelForm):

    name = StringField(_('Name'), [Optional(), Length(1, 255)])
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
    opening_time = TimeField(_('Business Open time'), [DataRequired()])
    closing_time = TimeField(_('Business Close time'), [DataRequired()])
    weekends_open = BooleanField(_('Yes, Open on weekends'))

    phone = StringField(_('Business Phone number'), [DataRequired(), Length(1, 12)])
    active = BooleanField(_('Yes, Business is active'))

    street = StringField(_('Street Address'), [DataRequired(), Length(1, 255)])
    city = StringField(_('City'), [DataRequired(), Length(1, 30)])
    state = StringField(_('State'), [DataRequired(), Length(1, 30)])
    zipcode = StringField(_('Zipcode'), [DataRequired(), Length(1, 30)])
    district = StringField(_('District/County'), [Optional(), Length(1, 30)])
    country = StringField(_('Country'), [DataRequired(), Length(1, 30)])


class EmployeeForm(ModelForm):
    name = StringField(_('Name'), [DataRequired(), Length(1, 255)])
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

    name = StringField(_('Product name'), [DataRequired(), Length(1, 255)])
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
    start_time = DateTimeField(_('Start time (in GMT timezone)'), [Optional()], format='%Y-%m-%d %H:%M:%S')
    end_time = DateTimeField(_('End time (in GMT timezone)'), [Optional()], format='%Y-%m-%d %H:%M:%S')
    status = SelectField(_('Reservation Status'), [DataRequired()],
                         choices=choices_from_dict(Reservation.STATUS,
                         prepend_blank=False))


class BookingForm(ModelForm):
    employee_id = HiddenField()
    start_time = DateTimeField(_('Start time'), [Optional()], format='%Y-%m-%d %H:%M:%S')
    end_time = DateTimeField(_('End time'), [Optional()], format='%Y-%m-%d %H:%M:%S')
