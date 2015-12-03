from flask import Blueprint, render_template
from flask_login import login_required

from cheermonk.blueprints.user.decorators import role_required

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
    return render_template('page/dashboard.jinja2')
