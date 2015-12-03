from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from sqlalchemy import text

from cheermonk.blueprints.user.decorators import role_required
from cheermonk.blueprints.dashboard.models import Dashboard
from cheermonk.blueprints.business.models.business import Business
from cheermonk.blueprints.user.models import User
from cheermonk.blueprints.admin.forms import SearchForm, BulkDeleteForm

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


# Businesses -----------------------------------------------------------------------
@dashboard.route('/businesses', defaults={'page': 1})
@dashboard.route('/businesses/page/<int:page>')
def businesses(page):
    search_form = SearchForm()
    bulk_form = BulkDeleteForm()

    sort_by = Business.sort_by(request.args.get('sort', 'name'),
                               request.args.get('direction', 'asc'))
    order_values = '{0} {1}'.format(sort_by[0], sort_by[1])

    paginated_businesses = Business.query \
        .filter(Business.search(request.args.get('q', ''))) \
        .filter(Business.admins.any(User.id.in_([current_user.id]))) \
        .order_by(Business.type.desc(), text(order_values)) \
        .paginate(page, 20, True)

    return render_template('admin/business/index.jinja2',
                           form=search_form, bulk_form=bulk_form,
                           businesses=paginated_businesses)
