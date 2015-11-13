from flask import (
    Blueprint,
    redirect,
    request,
    flash,
    url_for,
    render_template)
from flask_login import (
    login_required,
    login_user,
    logout_user)

from cheermonk.lib.safe_next_url import safe_next_url
from cheermonk.blueprints.user.decorators import anonymous_required
from cheermonk.blueprints.user.models import User
from cheermonk.blueprints.user.forms import (
    LoginForm,
    SignupForm
    )

user = Blueprint('user', __name__, template_folder='templates')


@user.route('/login', methods=['GET', 'POST'])
@anonymous_required()
def login():
    form = LoginForm(next=request.args.get('next'))

    if form.validate_on_submit():
        u = User.find_by_identity(request.form.get('identity'))

        if u and u.authenticated(password=request.form.get('password')):
            # As you can see remember me is always enabled, this was a design
            # decision I made because more often than not users want this
            # enabled. This allows for a less complicated login form.
            #
            # If however you want them to be able to select whether or not they
            # should remain logged in then perform the following 3 steps:
            # 1) Replace 'True' below with: request.form.get('remember', False)
            # 2) Uncomment the 'remember' field in user/forms.py#LoginForm
            # 3) Add a checkbox to the login form with the id/name 'remember'
            if login_user(u, remember=True):
                # Handle optionally redirecting to the next URL safely.
                next_url = request.form.get('next')
                if next_url:
                    return redirect(safe_next_url(next_url))

                return redirect(url_for('user.settings'))
            else:
                flash('This account has been disabled.', 'error')
        else:
            flash('Identity or password is incorrect.', 'error')

    return render_template('user/login.jinja2', form=form)


@user.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('user.login'))


@user.route('/signup', methods=['GET', 'POST'])
@anonymous_required()
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        u = User()

        form.populate_obj(u)
        u.password = User.encrypt_password(request.form.get('password', None))
        u.save()

        if login_user(u):
            flash('Awesome, thanks for signing up!', 'success')
            return redirect(url_for('user.welcome'))

    return render_template('user/signup.jinja2', form=form)


@user.route('/welcome', methods=['GET', 'POST'])
@login_required
def welcome():
    return "Welcome new user"


@user.route('/settings')
@login_required
def settings():
    return "Logged in user Dashboard"
