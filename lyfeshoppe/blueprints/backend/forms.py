import logging
from collections import OrderedDict
from lyfeshoppe.lib.util_wtforms import ModelForm

from flask_wtf import Form
from wtforms import SelectField, StringField, DateTimeField, BooleanField, TextAreaField
from wtforms_components import EmailField, IntegerField
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
    email = EmailField(_("What's your e-mail address?"),
                       [DataRequired(), Length(3, 254)])
    phone = StringField(_('Phone number'), [Optional(), Length(1, 12)])
    street = StringField(_('Full Street Address'), [Optional(), Length(1, 255)])
    city = StringField(_('City'), [Optional(), Length(1, 30)])
    state = StringField(_('State'), [Optional(), Length(1, 30)])
    zipcode = StringField(_('Zipcode'), [Optional(), Length(1, 30)])
    district = StringField(_('District/County'), [Optional(), Length(1, 30)])
    country = StringField(_('Country'), [Optional(), Length(1, 30)])


class BusinessForm(ModelForm):

    name = StringField(_('Business name'), [Optional(), Length(1, 255)])
    email = EmailField(_("What's your e-mail address?"),
                       [DataRequired(), Length(3, 254)])
    type = SelectField(_('Business Type'), [DataRequired()],
                       choices=choices_from_dict(Business.TYPE,
                                                 prepend_blank=False))
    open_time = DateTimeField(_('Business Open time'), [Optional()], format='%Y-%m-%d %H:%M:%S')
    close_time = DateTimeField(_('Business Open time'), [Optional()], format='%Y-%m-%d %H:%M:%S')

    phone = StringField(_('Business Phone number'), [Optional(), Length(1, 12)])
    active = BooleanField(_('Yes, Business is active'))

    street = StringField(_('Street Address'), [Optional(), Length(1, 255)])
    city = StringField(_('City'), [Optional(), Length(1, 30)])
    state = StringField(_('State'), [Optional(), Length(1, 30)])
    zipcode = StringField(_('Zipcode'), [Optional(), Length(1, 30)])
    district = StringField(_('District/County'), [Optional(), Length(1, 30)])
    country = StringField(_('Country'), [Optional(), Length(1, 30)])


class EmployeeForm(ModelForm):

    name = StringField(_('Employee name'), [DataRequired(), Length(1, 255)])
    email = EmailField(_("Employee e-mail address?"), [DataRequired(), Length(3, 254)])
    role = SelectField(_('Employee Role'), [DataRequired()],
                       choices=choices_from_dict(Employee.ROLE,
                                                 prepend_blank=False))
    active = BooleanField(_('Yes, Employee is active'))


class ProductForm(ModelForm):

    name = StringField(_('Product name'), [DataRequired(), Length(1, 255)])
    description = TextAreaField(_("Product description"), [DataRequired(), Length(3, 2048)])
    capacity = IntegerField(_('Service Capacity'), [Optional(), NumberRange(min=1, max=1000)])
    price_cents = IntegerField(_('Price in cents'), [Optional(), NumberRange(min=1, max=1000000)])
    duration_mins = IntegerField(_('Duration in mins'), [Optional(), NumberRange(min=1, max=1000)])

    active = BooleanField(_('Yes, Product is active'))


class ReservationForm(ModelForm):

    status = SelectField(_('Reservation Status'), [DataRequired()],
                         choices=choices_from_dict(Reservation.STATUS,
                         prepend_blank=False))
    start_time = DateTimeField(_('Reservation Start time'), [Optional()], format='%Y-%m-%d %H:%M:%S')
    end_time = DateTimeField(_('Reservation End time'), [Optional()], format='%Y-%m-%d %H:%M:%S')
