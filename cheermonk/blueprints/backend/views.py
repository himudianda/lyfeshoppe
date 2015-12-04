from flask import Blueprint, render_template
from flask_login import login_required

from cheermonk.blueprints.backend.models import Dashboard
from cheermonk.blueprints.user.decorators import role_required


backend = Blueprint('backend', __name__, template_folder='templates', url_prefix='/backend')


@backend.before_request
@login_required
@role_required('member')
def before_request():
    """ We are protecting all of our backend endpoints. """
    pass


# Dashboard -------------------------------------------------------------------
@backend.route('')
def dashboard():
    group_and_count_businesses = Dashboard.group_and_count_businesses()

    return render_template('page/dashboard.jinja2',
                           group_and_count_businesses=group_and_count_businesses)
