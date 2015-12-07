import logging
from collections import OrderedDict
from cheermonk.lib.util_wtforms import ModelForm

from flask_wtf import Form
from wtforms import SelectField, StringField, DateTimeField, BooleanField
from wtforms_components import EmailField
from wtforms.validators import DataRequired, Length, Optional
from flask_babel import lazy_gettext as _
from cheermonk.blueprints.business.models.business import Business

try:
    from instance import settings

    LANGUAGES = settings.LANGUAGES
except ImportError:
    logging.error('Ensure __init__.py and settings.py both exist in instance/')
    exit(1)
except AttributeError:
    from config import settings

    LANGUAGES = settings.LANGUAGES

from cheermonk.lib.util_wtforms import choices_from_dict


class SearchForm(Form):
    q = StringField(_('Search terms'), [Optional(), Length(1, 128)])


class BulkDeleteForm(Form):
    SCOPE = OrderedDict([
        ('all_selected_products', 'All selected items'),
        ('all_search_results', 'All search results')
    ])

    scope = SelectField(_('Privileges'), [DataRequired()],
                        choices=choices_from_dict(SCOPE, prepend_blank=False))


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
