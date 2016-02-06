import logging
from collections import OrderedDict

from flask_wtf import Form
from wtforms import SelectField, StringField, BooleanField, TextAreaField, \
    FloatField, DateTimeField
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, Optional, Regexp, \
    NumberRange
from wtforms_components import Unique, EmailField, IntegerField
from flask_babel import lazy_gettext as _

try:
    from instance import settings

    LANGUAGES = settings.LANGUAGES
except ImportError:
    logging.error('Ensure __init__.py and settings.py both exist in instance/')
    exit(1)
except AttributeError:
    from config import settings

    LANGUAGES = settings.LANGUAGES

from lyfeshoppe.lib.locale import Currency
from lyfeshoppe.lib.util_wtforms import ModelForm, choices_from_dict
from lyfeshoppe.blueprints.user.models import db, User
from lyfeshoppe.blueprints.business.models.business import Business
from lyfeshoppe.blueprints.issue.models import Issue


class SearchForm(Form):
    q = StringField(_('Search terms'), [Optional(), Length(1, 128)])


class BulkDeleteForm(Form):
    SCOPE = OrderedDict([
        ('all_selected_products', 'All selected items'),
        ('all_search_results', 'All search results')
    ])

    scope = SelectField(_('Privileges'), [DataRequired()],
                        choices=choices_from_dict(SCOPE, prepend_blank=False))


class UserForm(ModelForm):
    username_message = _('Letters, numbers and underscores only please.')

    username = StringField(validators=[
        Unique(
            User.username,
            get_session=lambda: db.session
        ),
        Optional(),
        Length(1, 16),
        Regexp('^\w+$', message=username_message)
    ])
    first_name = StringField(_('First name'), [Optional(), Length(1, 128)])
    last_name = StringField(_('Last name'), [Optional(), Length(1, 128)])
    role = SelectField(_('Privileges'), [DataRequired()],
                       choices=choices_from_dict(User.ROLE,
                                                 prepend_blank=False))
    active = BooleanField(_('Yes, allow this user to sign in'))
    locale = SelectField(_('Language preference'), [DataRequired()],
                         choices=choices_from_dict(LANGUAGES))


class BusinessForm(ModelForm):

    name = StringField(_('Business name'), [Optional(), Length(1, 255)])
    type = SelectField(_('Business Type'), [DataRequired()],
                       choices=choices_from_dict(Business.TYPE,
                                                 prepend_blank=False))
    admins = QuerySelectMultipleField(
      label="Admins",
      query_factory=lambda: User.query.all(),
      get_pk=lambda item: item.id,
      get_label=lambda item: item.name if item.name else item.email,
      allow_blank=True
    )

    employees = QuerySelectMultipleField(
      label="Employees",
      query_factory=lambda: User.query.all(),
      get_pk=lambda item: item.id,
      get_label=lambda item: item.name if item.name else item.email,
      allow_blank=True
    )


class UserCancelSubscriptionForm(Form):
    pass


class IssueForm(Form):
    label = SelectField(_('What do you need help with?'), [DataRequired()],
                        choices=choices_from_dict(Issue.LABEL))
    email = EmailField(_("What's your e-mail address?"),
                       [DataRequired(), Length(3, 254)])
    question = TextAreaField(_("What's your question or issue?"),
                             [DataRequired(), Length(1, 8192)])
    status = SelectField(_('What status is the issue in?'), [DataRequired()],
                         choices=choices_from_dict(Issue.STATUS,
                                                   prepend_blank=False))


class IssueContactForm(Form):
    subject = StringField(_('Subject'), [DataRequired(), Length(1, 254)])
    message = TextAreaField(_('Message to be sent'),
                            [DataRequired(), Length(1, 8192)])
