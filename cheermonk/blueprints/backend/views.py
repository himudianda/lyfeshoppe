from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import text
from flask_babel import ngettext as _n
from flask_babel import gettext as _
import pytz

from cheermonk.extensions import db
from cheermonk.blueprints.backend.models import Dashboard, BusinessDashboard
from cheermonk.blueprints.user.decorators import role_required
from cheermonk.blueprints.backend.forms import SearchForm, BulkDeleteForm, BusinessForm, EmployeeForm
from cheermonk.blueprints.business.models.business import Business, Employee
from cheermonk.blueprints.user.models import User

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

    user_employee_ids = [employee.id for employee in Employee.query.filter(Employee.user == current_user)]
    paginated_businesses = Business.query \
        .filter(Business.search(request.args.get('q', ''))) \
        .filter(Business.employees.any(Employee.id.in_(user_employee_ids))) \
        .order_by(Business.type.desc(), text(order_values)) \
        .paginate(page, 20, True)

    return render_template('backend/business/index.jinja2',
                           form=search_form, bulk_form=bulk_form,
                           businesses=paginated_businesses)


@backend.route('/businesses/bulk_deactivate', methods=['POST'])
def businesses_bulk_deactivate():
    form = BulkDeleteForm()

    if form.validate_on_submit():
        ids = Business.get_bulk_action_ids(request.form.get('scope'),
                                           request.form.getlist('bulk_ids'),
                                           query=request.args.get('q', ''))

        # Cant use the query in comments below; coz businesses_relationships & not just Business
        # has stuff to be deleted.
        # Business.query.filter(Business.id.in_(ids)).delete()
        # Hence use the below work-around.

        for id in ids:
            business = Business.query.get(id)
            business.active = not business.active

        # map(db.session.delete, [Business.query.get(id) for id in ids])
        db.session.commit()

        flash(_n('%(num)d business was deactivated.',
                 '%(num)d businesses were deactivated.',
                 num=len(ids)), 'success')
    else:
        flash(_('No businesses were deactivated, something went wrong.'), 'error')

    return redirect(url_for('backend.businesses'))


@backend.route('/businesses/new', methods=['GET', 'POST'])
def businesses_new():
    business = Business()
    form = BusinessForm(obj=business)

    if form.validate_on_submit():
        form.populate_obj(business)

        params = {
            'name': business.name,
            'email': business.email,
            'type': business.type,
            'open_time': business.open_time,
            'close_time': business.close_time,
            'phone': business.phone,
            'active': business.active
        }

        if Business.create(params):
            flash(_('Business has been created successfully.'), 'success')
            return redirect(url_for('backend.businesses'))

    return render_template('backend/business/new.jinja2', form=form, business=business)


# Business Dashboard -------------------------------------------------------------------
def is_staff_authorized(func):
    from functools import wraps

    @wraps(func)
    def func_wrapper(id, **kwargs):
        business = Business.query.get(id)
        if not business:
            flash(_('You do not have permission to do that.'), 'error')
            return redirect(url_for('backend.businesses'))

        employee = Employee.query.filter(
                        (Employee.user_id == current_user.id) & (Employee.business_id == business.id)
                    ).first()

        if not employee:
            flash(_('You do not have permission to do that.'), 'error')
            return redirect(url_for('backend.businesses'))

        if employee not in business.employees:
            flash(_('You do not have permission to do that.'), 'error')
            return redirect(url_for('backend.businesses'))

        # For API editing employee data
        if kwargs.get('employee_id', None):
            emp = Employee.query.filter(
                        (Employee.id == kwargs['employee_id']) & (Employee.business_id == business.id)
                    ).first()
            if not emp:
                flash(_('You do not have permission to do that.'), 'error')
                return redirect(url_for('backend.business_employees', id=id))

        return func(id, **kwargs)
    return func_wrapper


@backend.route('/businesses/<int:id>')
@is_staff_authorized
def business_dashboard(id):
    business = Business.query.get(id)

    group_and_count_employees = BusinessDashboard.group_and_count_employees(business)
    group_and_count_products = BusinessDashboard.group_and_count_products(business)

    return render_template('backend/business/dashboard.jinja2',
                           group_and_count_employees=group_and_count_employees,
                           group_and_count_products=group_and_count_products,
                           business=business)


@backend.route('/businesses/edit/<int:id>', methods=['GET', 'POST'])
@is_staff_authorized
def business_edit(id):
    business = Business.query.get(id)
    form = BusinessForm(obj=business)

    if form.validate_on_submit():
        form.populate_obj(business)

        if business.name == '':
            business.business = None

        if business.open_time:
            business.open_time = business.open_time.replace(
                tzinfo=pytz.UTC)

        if business.close_time:
            business.close_time = business.close_time.replace(
                tzinfo=pytz.UTC)

        business.save()

        flash(_('Business has been saved successfully.'), 'success')
        return redirect(url_for('backend.businesses'))

    return render_template('backend/business/edit.jinja2', form=form, business=business)


@backend.route('/businesses/<int:id>/employees', defaults={'page': 1})
@backend.route('/businesses/<int:id>/employees/page/<int:page>')
@is_staff_authorized
def business_employees(id, page):
    business = Business.query.get(id)
    search_form = SearchForm()
    bulk_form = BulkDeleteForm()

    sort_by = Employee.sort_by(request.args.get('sort', 'role'),
                               request.args.get('direction', 'asc'))
    order_values = '{0} {1}'.format(sort_by[0], sort_by[1])

    paginated_employees = Employee.query \
        .filter(Employee.search(request.args.get('q', ''))) \
        .filter(Employee.business == business) \
        .order_by(Employee.role.desc(), text(order_values)) \
        .paginate(page, 20, True)

    return render_template('backend/employee/index.jinja2',
                           form=search_form, bulk_form=bulk_form,
                           employees=paginated_employees,
                           business=business)


@backend.route('/businesses/<int:id>/employees/bulk_deactivate', methods=['POST'])
@is_staff_authorized
def business_employees_bulk_deactivate(id):
    form = BulkDeleteForm()

    if form.validate_on_submit():
        ids = Employee.get_bulk_action_ids(request.form.get('scope'),
                                           request.form.getlist('bulk_ids'),
                                           query=request.args.get('q', ''))

        for employee_id in ids:
            employee = Employee.query.get(employee_id)
            employee.active = not employee.active
        db.session.commit()

        flash(_n('%(num)d employee was deactivated.',
                 '%(num)d employees were deactivated.',
                 num=len(ids)), 'success')
    else:
        flash(_('No employees were deactivated, something went wrong.'), 'error')

    return redirect(url_for('backend.business_employees', id=id))


@backend.route('/businesses/<int:id>/employees/new', methods=['GET', 'POST'])
@is_staff_authorized
def business_employees_new(id):
    business = Business.query.get(id)

    employee = Employee()
    form = EmployeeForm(obj=employee)

    if form.validate_on_submit():
        form.populate_obj(employee)

        user_params = {
            'name': employee.name,
            'email': employee.email,
            'password': "password",
            'role': 'member',
            'active': '1'
        }

        if User.create(user_params):

            employee_params = {
                'role': employee.role,
                'business_id': id,
                'user_id': (User.query.filter(User.email == employee.email).first()).id
            }

            if Employee.create(employee_params):
                flash(_('Employee has been created successfully.'), 'success')
                return redirect(url_for('backend.business_employees', id=id))

    return render_template('backend/employee/new.jinja2', form=form, employee=employee, business=business)


@backend.route('/businesses/<int:id>/employees/edit/<int:employee_id>', methods=['GET', 'POST'])
@is_staff_authorized
def business_employee_edit(id, employee_id):
    business = Business.query.get(id)
    employee = Employee.query.get(employee_id)
    form = EmployeeForm(obj=employee)

    if form.validate_on_submit():
        form.populate_obj(employee)

        if employee.name == '':
            employee.name = None

        employee.save()

        flash(_('Employee has been saved successfully.'), 'success')
        return redirect(url_for('backend.business_employees', id=id))

    return render_template('backend/employee/edit.jinja2', form=form, business=business, employee=employee)
