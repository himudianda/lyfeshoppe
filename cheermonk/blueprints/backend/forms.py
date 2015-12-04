import logging
from collections import OrderedDict

from flask_wtf import Form
from wtforms import SelectField, StringField
from wtforms.validators import DataRequired, Length, Optional
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
