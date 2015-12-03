from flask import Blueprint, render_template
from flask_login import login_required

from cheermonk.blueprints.user.decorators import role_required
from cheermonk.blueprints.dashboard.models import Dashboard

dashboard = Blueprint('dashboard', __name__, template_folder='templates', url_prefix='/dashboard')


@dashboard.before_request
@login_required
@role_required('member')
def before_request():
    """ We are protecting all of our member dashboard endpoints. """
    pass


# Dashboard -------------------------------------------------------------------
@dashboard.route('')
def index():
    group_and_count_businesses = Dashboard.group_and_count_businesses()

    return render_template('dashboard/page/dashboard.jinja2',
                           group_and_count_businesses=group_and_count_businesses)
