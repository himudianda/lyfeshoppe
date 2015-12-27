from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import text
from flask_babel import ngettext as _n
from flask_babel import gettext as _
import pytz

from lyfeshoppe.extensions import db
from lyfeshoppe.blueprints.backend.models import BusinessDashboard
from lyfeshoppe.blueprints.user.decorators import role_required
from lyfeshoppe.blueprints.backend.forms import SearchForm, BulkDeleteForm, UserAccountForm, BusinessForm, \
    EmployeeForm, ProductForm, ReservationForm
from lyfeshoppe.blueprints.business.models.business import Business, Employee, Product, Reservation, Customer
from lyfeshoppe.blueprints.user.models import User

backend = Blueprint('backend', __name__, template_folder='templates')


@backend.before_request
@login_required
@role_required('member')
def before_request():
    """ We are protecting all of our backend endpoints. """
    pass


# Launchpad
@backend.route('/')
def launchpad():
    return render_template('backend/page/launchpad.jinja2')


# Shop -------------------------------------------------------------------
@backend.route('/shops', defaults={'page': 1})
@backend.route('/shops/page/<int:page>')
def shops_list(page):
    search_form = SearchForm()
    sort_by = Business.sort_by(request.args.get('sort', 'name'),
                               request.args.get('direction', 'asc'))
    order_values = '{0} {1}'.format(sort_by[0], sort_by[1])

    paginated_businesses = Business.query \
        .filter(Business.search(request.args.get('q', ''))) \
        .order_by(text(order_values)) \
        .paginate(page, 20, True)

    return render_template('backend/shop/index.jinja2',
                           form=search_form,
                           business_types=Business.TYPE,
                           businesses=paginated_businesses)


@backend.route('/shops/<string:id>')
def shop_details(id):
    business = Business.query.get(id)
    employees = list()
    for employee in business.employees:
        user = User.query.get(employee.user_id)
        item = {
            'name': user.name,
            'email': user.email,
            'city': user.address.city,
            'phone': user.phone,
            'services': ','.join([str(product.id) for product in employee.products]),
            'total_reservations': len(employee.reservations),
            'num_of_services': len(employee.products),
        }
        employees.append(item)
    return render_template('backend/shop/details.jinja2', business=business, employees=employees)


@backend.route('/shops/<string:id>/booking')
def shop_booking(id):
    business = Business.query.get(id)
    return render_template('backend/shop/booking.jinja2', business=business)


# Account -------------------------------------------------------------------
@backend.route('/account')
def account():
    return render_template('backend/account/profile.jinja2')


@backend.route('/account/settings', methods=['GET', 'POST'])
def account_settings():
    form = UserAccountForm(obj=current_user)

    form_data = {
        "street": current_user.address.street,
        "city": current_user.address.city,
        "state": current_user.address.state,
        "zipcode": current_user.address.zipcode,
        "district": current_user.address.district,
        "country": current_user.address.country,
    }

    form = UserAccountForm(**form_data)

    if form.validate_on_submit():
        form.populate_obj(current_user)
        current_user.save()
        flash(_('User Account has been saved successfully.'), 'success')
        return redirect(url_for('backend.account'))

    return render_template('backend/account/settings.jinja2', form=form)


# Purchases -------------------------------------------------------------------
@backend.route('/purchases', defaults={'page': 1})
@backend.route('/purchases/page/<int:page>')
def purchases(page):
    search_form = SearchForm()

    sort_by = Reservation.sort_by(request.args.get('created_on', 'status'),
                                  request.args.get('direction', 'asc'))
    order_values = '{0} {1}'.format(sort_by[0], sort_by[1])

    user_customer_ids = [customer.id for customer in Customer.query.filter(Customer.user == current_user)]
    paginated_reservations = Reservation.query \
        .filter(Reservation.customer_id.in_(user_customer_ids)) \
        .order_by(Reservation.status.desc(), text(order_values)) \
        .paginate(page, 20, True)

    return render_template('backend/purchase/index.jinja2',
                           form=search_form,
                           purchases=paginated_reservations)


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

        # For API editing product data
        if kwargs.get('product_id', None):
            emp = Product.query.filter(
                        (Product.id == kwargs['product_id']) & (Product.business_id == business.id)
                    ).first()
            if not emp:
                flash(_('You do not have permission to do that.'), 'error')
                return redirect(url_for('backend.business_products', id=id))

        # For API editing reservation data
        if kwargs.get('reservation_id', None):
            emp = Reservation.query.filter(
                        (Reservation.id == kwargs['reservation_id']) & (Reservation.business_id == business.id)
                    ).first()
            if not emp:
                flash(_('You do not have permission to do that.'), 'error')
                return redirect(url_for('backend.business_reservations', id=id))

        return func(id, **kwargs)
    return func_wrapper


@backend.route('/businesses/<int:id>')
@is_staff_authorized
def business_dashboard(id):
    business = Business.query.get(id)

    group_and_count_employees = BusinessDashboard.group_and_count_employees(business)
    group_and_count_products = BusinessDashboard.group_and_count_products(business)
    group_and_count_reservations = BusinessDashboard.group_and_count_reservations(business)

    return render_template('backend/business/dashboard.jinja2',
                           group_and_count_employees=group_and_count_employees,
                           group_and_count_products=group_and_count_products,
                           group_and_count_reservations=group_and_count_reservations,
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


# Business Employees -------------------------------------------------------------------
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

    form_data = {
        "name": employee.user.name,
        "email": employee.user.email,
        "role": employee.role,
        "active": employee.active
    }

    form = EmployeeForm(**form_data)

    if form.validate_on_submit():
        form.populate_obj(employee)

        if employee.name == '':
            employee.name = None

        employee.save()

        flash(_('Employee has been saved successfully.'), 'success')
        return redirect(url_for('backend.business_employees', id=id))

    return render_template('backend/employee/edit.jinja2', form=form, business=business, employee=employee)


# Business Products -------------------------------------------------------------------
@backend.route('/businesses/<int:id>/products', defaults={'page': 1})
@backend.route('/businesses/<int:id>/products/page/<int:page>')
@is_staff_authorized
def business_products(id, page):
    business = Business.query.get(id)
    search_form = SearchForm()
    bulk_form = BulkDeleteForm()

    sort_by = Product.sort_by(request.args.get('sort', 'capacity'),
                              request.args.get('direction', 'asc'))
    order_values = '{0} {1}'.format(sort_by[0], sort_by[1])

    paginated_products = Product.query \
        .filter(Product.search(request.args.get('q', ''))) \
        .filter(Product.business == business) \
        .order_by(Product.price_cents.desc(), text(order_values)) \
        .paginate(page, 20, True)

    return render_template('backend/product/index.jinja2',
                           form=search_form, bulk_form=bulk_form,
                           products=paginated_products,
                           business=business)


@backend.route('/businesses/<int:id>/products/bulk_deactivate', methods=['POST'])
@is_staff_authorized
def business_products_bulk_deactivate(id):
    form = BulkDeleteForm()

    if form.validate_on_submit():
        ids = Product.get_bulk_action_ids(request.form.get('scope'),
                                          request.form.getlist('bulk_ids'),
                                          query=request.args.get('q', ''))

        for product_id in ids:
            product = Product.query.get(product_id)
            product.active = not product.active
        db.session.commit()

        flash(_n('%(num)d product was deactivated.',
                 '%(num)d products were deactivated.',
                 num=len(ids)), 'success')
    else:
        flash(_('No products were deactivated, something went wrong.'), 'error')

    return redirect(url_for('backend.business_products', id=id))


@backend.route('/businesses/<int:id>/products/new', methods=['GET', 'POST'])
@is_staff_authorized
def business_products_new(id):
    business = Business.query.get(id)

    product = Product()
    form = ProductForm(obj=product)

    if form.validate_on_submit():
        form.populate_obj(product)

        params = {
            'name': product.name,
            'description': product.description,
            'capacity': product.capacity,
            'price_cents': product.price_cents,
            'duration_mins': product.duration_mins,
            'active': '1',
            'business_id': id
        }

        if Product.create(params):
            flash(_('Product has been created successfully.'), 'success')
            return redirect(url_for('backend.business_products', id=id))

    return render_template('backend/product/new.jinja2', form=form, product=product, business=business)


@backend.route('/businesses/<int:id>/products/edit/<int:product_id>', methods=['GET', 'POST'])
@is_staff_authorized
def business_product_edit(id, product_id):
    business = Business.query.get(id)
    product = Product.query.get(product_id)

    form_data = {
        "name": product.name,
        "description": product.description,
        "capacity": product.capacity,
        "price_cents": product.price_cents,
        "duration_mins": product.duration_mins,
        "active": product.active
    }

    form = ProductForm(**form_data)

    if form.validate_on_submit():
        form.populate_obj(product)

        if product.name == '':
            product.name = None

        product.save()

        flash(_('Product has been saved successfully.'), 'success')
        return redirect(url_for('backend.business_products', id=id))

    return render_template('backend/product/edit.jinja2', form=form, business=business, product=product)


# Business Reservations -------------------------------------------------------------------
@backend.route('/businesses/<int:id>/reservations', defaults={'page': 1})
@backend.route('/businesses/<int:id>/reservations/page/<int:page>')
@is_staff_authorized
def business_reservations(id, page):
    business = Business.query.get(id)
    search_form = SearchForm()
    bulk_form = BulkDeleteForm()

    sort_by = Reservation.sort_by(request.args.get('created_on', 'status'),
                                  request.args.get('direction', 'asc'))
    order_values = '{0} {1}'.format(sort_by[0], sort_by[1])

    paginated_reservations = Reservation.query \
        .filter(Reservation.business == business) \
        .order_by(Reservation.status.desc(), text(order_values)) \
        .paginate(page, 20, True)

    return render_template('backend/reservation/index.jinja2',
                           form=search_form, bulk_form=bulk_form,
                           reservations=paginated_reservations,
                           business=business)


@backend.route('/businesses/<int:id>/reservations/new', methods=['GET', 'POST'])
@is_staff_authorized
def business_reservations_new(id):

    business = Business.query.get(id)

    reservation = Reservation()
    form = ReservationForm(obj=reservation)

    if form.validate_on_submit():
        form.populate_obj(reservation)

        params = {
            'status': reservation.status,
            'start_time': reservation.start_time,
            'end_time': reservation.end_time,
            'business_id': id
        }

        if Reservation.create(params):
            flash(_('Reservation has been created successfully.'), 'success')
            return redirect(url_for('backend.business_reservations', id=id))

    return render_template('backend/reservation/new.jinja2', form=form, reservation=reservation, business=business)


@backend.route('/businesses/<int:id>/reservations/edit/<int:reservation_id>', methods=['GET', 'POST'])
@is_staff_authorized
def business_reservation_edit(id, reservation_id):
    business = Business.query.get(id)
    reservation = Reservation.query.get(reservation_id)

    form_data = {
        "status": reservation.status,
        "start_time": reservation.start_time,
        "end_time": reservation.end_time,
    }

    form = ReservationForm(**form_data)

    if form.validate_on_submit():
        form.populate_obj(reservation)

        if reservation.start_time:
            reservation.start_time = reservation.start_time.replace(
                tzinfo=pytz.UTC)

        if reservation.end_time:
            reservation.end_time = reservation.end_time.replace(
                tzinfo=pytz.UTC)

        reservation.save()

        flash(_('Reservation has been saved successfully.'), 'success')
        return redirect(url_for('backend.business_reservations', id=id))

    return render_template('backend/reservation/edit.jinja2', form=form, business=business, reservation=reservation)
