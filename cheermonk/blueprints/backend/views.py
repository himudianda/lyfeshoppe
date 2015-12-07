from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import text
from flask_babel import ngettext as _n
from flask_babel import gettext as _

from cheermonk.extensions import db
from cheermonk.blueprints.backend.models import Dashboard
from cheermonk.blueprints.user.decorators import role_required
from cheermonk.blueprints.backend.forms import SearchForm, BulkDeleteForm
from cheermonk.blueprints.business.models.business import Business, Employee

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

    return render_template('backend/page/dashboard.jinja2',
                           group_and_count_businesses=group_and_count_businesses)


# Businesses -----------------------------------------------------------------------
@backend.route('/businesses', defaults={'page': 1})
@backend.route('/businesses/page/<int:page>')
def businesses(page):
    search_form = SearchForm()
    bulk_form = BulkDeleteForm()

    sort_by = Business.sort_by(request.args.get('sort', 'name'),
                               request.args.get('direction', 'asc'))
    order_values = '{0} {1}'.format(sort_by[0], sort_by[1])

    paginated_businesses = Business.query \
        .filter(Business.search(request.args.get('q', ''))) \
        .filter(Business.employees.any(Employee.id.in_([current_user.id]))) \
        .order_by(Business.type.desc(), text(order_values)) \
        .paginate(page, 20, True)

    return render_template('backend/business/index.jinja2',
                           form=search_form, bulk_form=bulk_form,
                           businesses=paginated_businesses)


# Dashboard -------------------------------------------------------------------
@backend.route('/businesses/<int:id>')
def business_dashboard(id):
    business = Business.query.get(id)
    group_and_count_businesses = Dashboard.group_and_count_businesses()

    return render_template('backend/business/dashboard.jinja2',
                           group_and_count_businesses=group_and_count_businesses)


@backend.route('/businesses/bulk_delete', methods=['POST'])
def businesses_bulk_delete():
    form = BulkDeleteForm()

    if form.validate_on_submit():
        ids = Business.get_bulk_action_ids(request.form.get('scope'),
                                           request.form.getlist('bulk_ids'),
                                           query=request.args.get('q', ''))

        # Cant use the query in comments below; coz businesses_relationships & not just Business
        # has stuff to be deleted.
        # Business.query.filter(Business.id.in_(ids)).delete()
        # Hence use the below work-around.

        map(db.session.delete, [Business.query.get(id) for id in ids])
        db.session.commit()

        flash(_n('%(num)d business was deleted.',
                 '%(num)d businesses were deleted.',
                 num=len(ids)), 'success')
    else:
        flash(_('No businesses were deleted, something went wrong.'), 'error')

    return redirect(url_for('backend.businesses'))
