from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import text
from flask_babel import ngettext as _n
from flask_babel import gettext as _
import json

from lyfeshoppe.extensions import db
from lyfeshoppe.blueprints.backend.models import BusinessDashboard
from lyfeshoppe.blueprints.user.decorators import role_required
from lyfeshoppe.blueprints.backend.forms import SearchForm, BulkDeleteForm, UserAccountForm, BusinessForm, \
    EmployeeForm, ProductForm, ReservationForm, ReservationEditForm, BookingForm, CustomerForm, ReviewForm
from lyfeshoppe.blueprints.user.forms import PasswordResetForm
from lyfeshoppe.blueprints.business.models.business import Business, Employee, Product, Reservation, Customer, Review
from lyfeshoppe.blueprints.user.models import User

backend = Blueprint('backend', __name__, template_folder='templates')

business_categories = dict(
    business_services=Business.SERVICES,
    business_types=Business.TYPE,
    business_service_types=Business.SERVICE_TYPES
)


@backend.before_request
@login_required
@role_required('member')
def before_request():
    """ We are protecting all of our backend endpoints. """
    pass


# Launchpad
@backend.route('/welcome')
def launchpad():
    return render_template('backend/page/launchpad.jinja2')


# Shop -------------------------------------------------------------------
@backend.route('/shops', defaults={'type': "makeup", 'page': 1})
@backend.route('/shops/type/<string:type>', defaults={'page': 1})
@backend.route('/shops/type/<string:type>/page/<int:page>')
def shops_list(page, type):
    search_form = SearchForm()
    sort_by = Business.sort_by(request.args.get('sort', 'name'),
                               request.args.get('direction', 'asc'))
    order_values = '{0} {1}'.format(sort_by[0], sort_by[1])

    paginated_businesses = Business.query \
        .filter(Business.search(request.args.get('q', '')), Business.type == type) \
        .filter(Business.active) \
        .order_by(text(order_values)) \
        .paginate(page, 120, True)

    type_images = Business.type_images(type)

    return render_template('backend/shop/index.jinja2',
                           form=search_form,
                           businesses=paginated_businesses,
                           metros=Business.METRO,
                           type=type,
                           type_images=type_images,
                           **business_categories)


@backend.route('/shops/<string:id>')
def shop_details(id):
    business = Business.query.get(id)
    employees = list()
    for employee in business.active_employees:
        user = User.query.get(employee.user_id)
        item = {
            'id': employee.id,
            'name': user.name,
            'email': user.email,
            'about': employee.about,
            'city': user.address.city if user.address else "Unknown",
            'phone': user.phone,
            'total_reservations': len(employee.reservations),
            'num_of_services': len(employee.products),
            'rating': employee.rating,
            'reviews': employee.reviews
        }
        employees.append(item)

    products = dict()
    for product in business.products:
        if product.category not in products:
            products[product.category] = []
        products[product.category].append(product)

    type_images = Business.type_images(business.type)

    return render_template(
                'backend/shop/details.jinja2',
                business=business, employees=employees,
                products=products,
                type_images=type_images,
                **business_categories)


@backend.route('/shops/<string:id>/product/<string:product_id>/booking', methods=['GET', 'POST'])
def shop_booking(id, product_id):
    business = Business.query.get(id)
    product = Product.query.filter(Product.id == product_id, Product.business_id == id).first()

    form = BookingForm()
    if form.is_submitted() and form.validate_on_submit():

        reservation = Reservation()
        form.populate_obj(reservation)

        params = {
            'status': 'new',  # Since this reservation was made by customer - mark as new
            'customer_email': current_user.email,
            'employee_id': request.form.get('employee_id'),
            'product_id': product_id,
            'business_id': id,
            'start_time': reservation.start_time,
            'end_time': reservation.end_time
        }

        if Reservation.create(params):
            flash(_('Reservation has been created successfully.'), 'success')
            return redirect(url_for('backend.shop_details', id=id))
        else:
            flash(_('Reservation create failed.'), 'error')
            return redirect(url_for('backend.shop_details', id=id))

    events = dict()

    # Note: A new employee may have no reservations & on the frontend
    # we want to have his calendar displayed. Hence this step
    for employee in business.active_employees:
        employee_id = str(employee.id)
        if employee_id not in events:
            events[employee_id] = []

    for reservation in business.reservations:
        # Note: isoformat() function below tells the browser javascript that the time is in UTC.
        # Else; It is taken as Local timezone.
        employee_id = str(reservation.employee.id)
        if employee_id in events:  # Inactive employee ID may not exist in events - so this check is required
            events[employee_id].append({
                "title": reservation.product.name,
                "start": reservation.start_time.isoformat(),
                "end": reservation.end_time.isoformat(),
                "allDay": False,
                "status": Reservation.STATUS[reservation.status],
                "backgroundColor": Reservation.STATUS_COLORS[reservation.status],
                "reservation_id": str(reservation.id)
            })

    return render_template('backend/shop/booking.jinja2',
                           form=form,
                           business=business, product=product,
                           events=json.dumps(events),
                           **business_categories)


@backend.route('/shops/<string:id>/employee/<string:employee_id>/review', methods=['GET', 'POST'])
def shop_reviews_new(id, employee_id):
    business = Business.query.get(id)
    employee = Employee.query.filter(Employee.id == employee_id, Employee.business_id == id).first()
    customer = Customer.query.filter(Customer.user_id == current_user.id, Customer.business_id == id).first()

    if not business or not employee:
        flash(_('Business or Employee does not exist.'), 'error')
        return redirect(url_for('backend.shop_details', id=id))

    if not customer:
        flash(_('You must be a customer to write a review.'), 'error')
        return redirect(url_for('backend.shop_details', id=id))

    form = ReviewForm()
    if form.is_submitted() and form.validate_on_submit():

        if Review.create_from_form(id, employee_id, customer.id, form):
            flash(_('Review has been created successfully.'), 'success')
            return redirect(url_for('backend.shop_details', id=id))

    return render_template('backend/shop/review_add.jinja2',
                           form=form,
                           business=business, employee=employee,
                           **business_categories)


# Account -------------------------------------------------------------------
@backend.route('/account/settings', methods=['GET', 'POST'])
def account_settings():
    address_dict = {}
    if current_user.address:
        address_dict = current_user.address.__dict__

    form = UserAccountForm(obj=current_user, **address_dict)
    password_reset_form = PasswordResetForm()

    # form.is_submitted() ensures that this block of code is
    # only triggered if this form was submitted
    if form.is_submitted() and form.validate_on_submit():
        if current_user.modify_from_form(form):
            flash(_('User Account has been modified successfully.'), 'success')
            return redirect(url_for('backend.account_settings'))

    if password_reset_form.is_submitted() and password_reset_form.validate_on_submit():
        password_reset_form.populate_obj(current_user)
        current_user.password = User.encrypt_password(request.form.get('password', None))
        current_user.save()

        flash(_('Your password has been reset.'), 'success')
        return redirect(url_for('backend.account_settings'))

    return render_template(
                'backend/account/settings.jinja2',
                form=form, password_reset_form=password_reset_form,
                **business_categories)


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
                           purchases=paginated_reservations,
                           **business_categories)


# Shop Reviews -------------------------------------------------------------------
@backend.route('/reviews', defaults={'page': 1})
@backend.route('/reviews/page/<int:page>')
def reviews(page):
    search_form = SearchForm()

    sort_by = Review.sort_by(request.args.get('created_on', 'status'),
                             request.args.get('direction', 'asc'))
    order_values = '{0} {1}'.format(sort_by[0], sort_by[1])

    user_customer_ids = [customer.id for customer in Customer.query.filter(Customer.user == current_user)]
    paginated_reviews = Review.query \
        .filter(Review.customer_id.in_(user_customer_ids)) \
        .order_by(Review.status.desc(), text(order_values)) \
        .paginate(page, 20, True)

    return render_template('backend/shop/review_index.jinja2',
                           form=search_form,
                           reviews=paginated_reviews,
                           **business_categories)


@backend.route('/reviews/edit/<int:id>', methods=['GET', 'POST'])
def review_edit(id):
    review = Review.query.get(id)
    if review.customer.user_id != current_user.id:
        flash(_('You are not permitted to edit this review.'), 'error')
        return redirect(url_for('backend.reviews'))

    form = ReviewForm(obj=review)

    if form.validate_on_submit():
        if review.modify_from_form(form):
            flash(_('Review has been modified successfully.'), 'success')
            if current_user.role == "admin":
                return redirect(url_for('admin.reviews'))
            return redirect(url_for('backend.reviews'))

    return render_template('backend/shop/review_edit.jinja2', form=form,
                           review=review,
                           **business_categories)


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
                           businesses=paginated_businesses,
                           **business_categories)


@backend.route('/businesses/new', methods=['GET', 'POST'])
def businesses_new():
    business = Business()
    form = BusinessForm(obj=business)

    if form.validate_on_submit():
        if Business.create_from_form(form):
            flash(_('Business has been created successfully.'), 'success')
            return redirect(url_for('backend.businesses'))

    return render_template('backend/business/new.jinja2', form=form, business=business, **business_categories)


# Business Dashboard -------------------------------------------------------------------
def is_staff_authorized(func):
    from functools import wraps

    @wraps(func)
    def func_wrapper(id, **kwargs):
        business = Business.query.get(id)
        if not business:
            flash(_('Invalid Business ID provided.'), 'error')
            return redirect(url_for('backend.businesses'))

        if current_user.role == "admin":
            return func(id, **kwargs)

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
            product = Product.query.filter(
                        (Product.id == kwargs['product_id']) & (Product.business_id == business.id)
                    ).first()
            if not product:
                flash(_('You do not have permission to do that.'), 'error')
                return redirect(url_for('backend.business_products', id=id))

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
    address_dict = dict()
    if business.address:
        address_dict = business.address.__dict__

    form = BusinessForm(obj=business, **address_dict)

    if form.validate_on_submit():
        if business.modify_from_form(form):
            flash(_('Business has been modified successfully.'), 'success')
            if current_user.role == "admin":
                return redirect(url_for('admin.businesses'))
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
        employee, created = Employee.get_or_create(business_id=id, params=None, from_form=True, form=form)
        if created:
            flash(_('Employee has been created successfully.'), 'success')
            return redirect(url_for('backend.business_employees', id=id))
        else:
            flash(_('Employee already exists.'), 'success')
            return redirect(url_for('backend.business_employees', id=id))

    return render_template('backend/employee/new.jinja2', form=form, employee=employee, business=business)


@backend.route('/businesses/<int:id>/employees/edit/<int:employee_id>', methods=['GET', 'POST'])
@is_staff_authorized
def business_employee_edit(id, employee_id):
    business = Business.query.get(id)
    employee = Employee.query.get(employee_id)

    form_data = dict()
    form_data.update(employee.user.__dict__)
    if employee.user.address:
        form_data.update(employee.user.address.__dict__)
    form = EmployeeForm(obj=employee, **form_data)

    if form.is_submitted() and form.validate_on_submit():
        if employee.modify_from_form(form):
            flash(_('Employee has been modified successfully.'), 'success')
            return redirect(url_for('backend.business_employees', id=id))

    return render_template('backend/employee/edit.jinja2', form=form, business=business, employee=employee)


# Business Customers -------------------------------------------------------------------
@backend.route('/businesses/<int:id>/customers', defaults={'page': 1})
@backend.route('/businesses/<int:id>/customers/page/<int:page>')
@is_staff_authorized
def business_customers(id, page):
    business = Business.query.get(id)
    search_form = SearchForm()
    bulk_form = BulkDeleteForm()

    sort_by = Customer.sort_by(request.args.get('sort', 'role'),
                               request.args.get('direction', 'asc'))
    order_values = '{0} {1}'.format(sort_by[0], sort_by[1])

    paginated_customers = Customer.query \
        .filter(Customer.search(request.args.get('q', ''))) \
        .filter(Customer.business == business) \
        .order_by(text(order_values)) \
        .paginate(page, 20, True)

    return render_template('backend/customer/index.jinja2',
                           form=search_form, bulk_form=bulk_form,
                           customers=paginated_customers,
                           business=business)


@backend.route('/businesses/<int:id>/customers/bulk_deactivate', methods=['POST'])
@is_staff_authorized
def business_customers_bulk_deactivate(id):
    form = BulkDeleteForm()

    if form.validate_on_submit():
        ids = Customer.get_bulk_action_ids(request.form.get('scope'),
                                           request.form.getlist('bulk_ids'),
                                           query=request.args.get('q', ''))

        for customer_id in ids:
            customer = Customer.query.get(customer_id)
            customer.active = not customer.active
        db.session.commit()

        flash(_n('%(num)d customer was deactivated.',
                 '%(num)d customer were deactivated.',
                 num=len(ids)), 'success')
    else:
        flash(_('No customers were deactivated, something went wrong.'), 'error')

    return redirect(url_for('backend.business_customers', id=id))


@backend.route('/businesses/<int:id>/customers/new', methods=['GET', 'POST'])
@is_staff_authorized
def business_customers_new(id):
    business = Business.query.get(id)
    customer = Customer()
    form = CustomerForm(obj=customer)

    if form.validate_on_submit():
        customer, created = Customer.get_or_create_from_form(business_id=id, form=form)
        if created:
            flash(_('Customer has been created successfully.'), 'success')
            return redirect(url_for('backend.business_customers', id=id))
        else:
            flash(_('Customer already exists.'), 'success')
            return redirect(url_for('backend.business_customers', id=id))

    return render_template('backend/customer/new.jinja2', form=form, customer=customer, business=business)


@backend.route('/businesses/<int:id>/customers/edit/<int:customer_id>', methods=['GET', 'POST'])
@is_staff_authorized
def business_customer_edit(id, customer_id):
    business = Business.query.get(id)
    customer = Customer.query.get(customer_id)

    form_data = dict()
    form_data.update(customer.user.__dict__)
    if customer.user.address:
        form_data.update(customer.user.address.__dict__)
    form = CustomerForm(obj=customer, **form_data)

    if form.is_submitted() and form.validate_on_submit():
        if customer.modify_from_form(form):
            flash(_('Customer has been modified successfully.'), 'success')
            return redirect(url_for('backend.business_customers', id=id))

    return render_template('backend/customer/edit.jinja2', form=form, business=business, customer=customer)


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
        if Product.create_from_form(business_id=id, form=form):
            flash(_('Product has been created successfully.'), 'success')
            return redirect(url_for('backend.business_products', id=id))

    return render_template('backend/product/new.jinja2', form=form, product=product, business=business)


@backend.route('/businesses/<int:id>/products/edit/<int:product_id>', methods=['GET', 'POST'])
@is_staff_authorized
def business_product_edit(id, product_id):
    business = Business.query.get(id)
    product = Product.query.get(product_id)
    form = ProductForm(obj=product)

    if form.is_submitted() and form.validate_on_submit():
        if product.modify_from_form(form):
            flash(_('Product has been modified successfully.'), 'success')
            return redirect(url_for('backend.business_products', id=id))

    return render_template('backend/product/edit.jinja2', form=form, business=business, product=product)


# Business Products -------------------------------------------------------------------
@backend.route('/businesses/<int:id>/reviews', defaults={'page': 1})
@backend.route('/businesses/<int:id>/reviews/page/<int:page>')
@is_staff_authorized
def business_reviews(id, page):
    business = Business.query.get(id)
    search_form = SearchForm()

    sort_by = Review.sort_by(request.args.get('sort', 'status'),
                             request.args.get('direction', 'asc'))
    order_values = '{0} {1}'.format(sort_by[0], sort_by[1])

    paginated_reviews = Review.query \
        .filter(Review.search(request.args.get('q', ''))) \
        .filter(Review.business == business) \
        .order_by(Review.product_id.desc(), text(order_values)) \
        .paginate(page, 20, True)

    return render_template('backend/review/index.jinja2',
                           form=search_form,
                           reviews=paginated_reviews,
                           business=business)


# Business Calendar -------------------------------------------------------------------
@backend.route('/businesses/<int:id>/calendar/<string:call>', methods=['GET', 'POST'])
@is_staff_authorized
def business_calendar(id, call):
    business = Business.query.get(id)
    form = ReservationForm()
    edit_form = ReservationEditForm()

    if call == "add" and form.is_submitted() and form.validate_on_submit():
        reservation = Reservation()
        form.populate_obj(reservation)

        params = {
            'status': 'confirmed',  # Since this reservation was made my employee - mark as confirmed
            'customer_email': request.form.get('customer_email'),
            'employee_id': request.form.get('employee_id'),
            'product_id': request.form.get('product_id'),
            'business_id': id,
            'start_time': reservation.start_time,
            'end_time': reservation.end_time
        }

        if Reservation.create(params):
            flash(_('Reservation has been created successfully.'), 'success')
            return redirect(url_for('backend.business_calendar', id=id, call="view"))
        else:
            flash(_('Reservation create failed.'), 'error')
            return redirect(url_for('backend.business_calendar', id=id, call="view"))

    if call == "edit" and edit_form.is_submitted() and edit_form.validate_on_submit():
        reservation_id = request.form.get('reservation_id'),
        reservation = Reservation.query.get_or_404(reservation_id)

        reservation.status = request.form.get('status')

        reservation.save()
        flash(_('Reservation has been saved modified.'), 'success')
        return redirect(url_for('backend.business_calendar', id=id, call="view"))

    events = dict()

    # Note: A new employee may have no reservations & on the frontend
    # we want to have his calendar displayed. Hence this step
    for employee in business.employees:
        employee_id = str(employee.id)
        if employee_id not in events:
            events[employee_id] = []

    for reservation in business.reservations:
        # Note: isoformat() function below tells the browser javascript that the time is in UTC.
        # Else; It is taken as Local timezone.
        employee_id = str(reservation.employee.id)
        events[employee_id].append({
            "title": reservation.product.name,
            "start": reservation.start_time.isoformat(),
            "end": reservation.end_time.isoformat(),
            "allDay": False,
            "status": reservation.status,
            "backgroundColor": Reservation.STATUS_COLORS[reservation.status],
            "reservation_id": str(reservation.id)
        })

    return render_template('backend/business/calendar.jinja2',
                           form=form, edit_form=edit_form,
                           business=business, events=json.dumps(events)
                           )
