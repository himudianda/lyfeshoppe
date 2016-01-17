from flask import Blueprint, redirect, request, flash, url_for, render_template
from flask_login import login_required, login_user, current_user, logout_user
from flask_babel import gettext as _

from lyfeshoppe.lib.safe_next_url import safe_next_url
from lyfeshoppe.lib.role_redirects import get_dashboard_url
from lyfeshoppe.lib.oauth_providers import OAuthSignIn
from lyfeshoppe.blueprints.user.decorators import anonymous_required
from lyfeshoppe.blueprints.user.models import User
from lyfeshoppe.blueprints.user.forms import LoginForm, BeginPasswordResetForm, PasswordResetForm, SignupForm, \
    WelcomeForm, UpdateCredentials, UpdateLocale

user = Blueprint('user', __name__, template_folder='templates')


@user.route('/authorize/<provider>')
@anonymous_required()
def oauth_authorize(provider):
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@user.route('/callback/<provider>')
@anonymous_required()
def oauth_callback(provider):
    oauth = OAuthSignIn.get_provider(provider)
    user_data = oauth.callback()
    provider = user_data.get('type', None)

    # Some validations
    if provider == 'facebook':
        if not user_data.get('id', None):
            flash(_('Facebook Authentication failed.'), 'error')
            return redirect(url_for('user.signup'))

        if not user_data.get('email', None):
            flash(_('Facebook login failed. Your email was not received from facebook.'), 'error')
            return redirect(url_for('user.signup'))

        if not user_data.get('name', None):
            flash(_('Facebook login failed. Your full name is not registered with Facebook.'), 'error')
            return redirect(url_for('user.signup'))

    # Validations done; now save user data
    if provider == 'facebook':
        params = {
            "social_id": provider + '$' + user_data['id'],
            "fb_id": provider + '$' + user_data['id'],
            "fb_link": user_data.get('link', None),
            "fb_verified": user_data.get('verified', False),
            "fb_added": True,
            "first_name": user_data.get('first_name', None),
            "last_name": user_data.get('last_name', None),
            "age_range_min": user_data['age_range'].get('min', None) if user_data.get('age_range', None) else None,
            "age_range_max": user_data['age_range'].get('max', None) if user_data.get('age_range', None) else None,
            "gender": user_data.get('gender', None),
            "timezone": user_data.get('timezone', None),
            "locale": user_data.get('locale', None),
            "email": user_data['email']
        }

        user = User.find_by_identity(user_data['email'])
        if not user:
            user = User.create(**params)
        else:
            # Check user has facebook data populated. If not populate it now
            if not user.fb_added and not user.fb_id:
                user.update(**params)
    else:
        flash(_('Facebook Authentication failed.'), 'error')
        return redirect(url_for('user.signup'))

    login_user(user, True)
    return redirect(get_dashboard_url())


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
                u.update_activity_tracking(request.remote_addr)

                # Handle optionally redirecting to the next URL safely.
                next_url = request.form.get('next')
                if next_url:
                    return redirect(safe_next_url(next_url))

                return redirect(get_dashboard_url())
            else:
                flash(_('This account has been disabled.'), 'error')
        else:
            flash(_('Email/password is incorrect OR try social (facebook) login.'), 'error')

    return render_template('user/login.jinja2', form=form)


@user.route('/logout')
@login_required
def logout():
    logout_user()
    flash(_('You have been logged out.'), 'success')
    return redirect(url_for('user.login'))


@user.route('/account/begin_password_reset', methods=['GET', 'POST'])
@anonymous_required()
def begin_password_reset():
    form = BeginPasswordResetForm()

    if form.validate_on_submit():
        u = User.initialize_password_reset(request.form.get('identity'))

        flash(_('An email has been sent to %(email)s.',
                email=u.email), 'success')
        return redirect(url_for('user.login'))

    return render_template('user/begin_password_reset.jinja2', form=form)


@user.route('/account/password_reset', methods=['GET', 'POST'])
@anonymous_required()
def password_reset():
    form = PasswordResetForm(reset_token=request.args.get('reset_token'))

    if form.validate_on_submit():
        u = User.deserialize_token(request.form.get('reset_token'))

        if u is None:
            flash(_('Your reset token has expired or was tampered with.'),
                  'error')
            return redirect(url_for('user.begin_password_reset'))

        form.populate_obj(u)
        u.password = User.encrypt_password(request.form.get('password', None))
        u.save()

        if login_user(u):
            flash(_('Your password has been reset.'), 'success')
            return redirect(get_dashboard_url())

    return render_template('user/password_reset.jinja2', form=form)


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
            flash(_('Awesome, thanks for signing up!'), 'success')
            return redirect(get_dashboard_url())

    return render_template('user/signup.jinja2', form=form)


@user.route('/welcome', methods=['GET', 'POST'])
@login_required
def welcome():
    if current_user.username:
        flash(_('You already picked a username.'), 'warning')
        return redirect(url_for('user.settings'))

    form = WelcomeForm()

    if form.validate_on_submit():
        current_user.username = request.form.get('username')
        current_user.save()

        flash(_('Sign up is complete, enjoy our services.'), 'success')
        return redirect(url_for('billing.pricing'))

    return render_template('user/welcome.jinja2', form=form)


@user.route('/settings')
@login_required
def settings():
    return render_template('user/settings.jinja2')


@user.route('/settings/update_credentials', methods=['GET', 'POST'])
@login_required
def update_credentials():
    form = UpdateCredentials(current_user, uid=current_user.id)

    if form.validate_on_submit():
        # We cannot form.populate_obj() because the password is optional.
        new_password = request.form.get('password', '')
        current_user.email = request.form.get('email')

        if new_password:
            current_user.password = User.encrypt_password(new_password)

        current_user.save()

        flash(_('Your sign in settings have been updated.'), 'success')
        return redirect(url_for('user.settings'))

    return render_template('user/update_credentials.jinja2', form=form)


@user.route('/settings/update_locale', methods=['GET', 'POST'])
@login_required
def update_locale():
    form = UpdateLocale(locale=current_user.locale)

    if form.validate_on_submit():
        form.populate_obj(current_user)
        current_user.save()

        flash(_('Your locale settings have been updated.'), 'success')
        return redirect(url_for('user.settings'))

    return render_template('user/update_locale.jinja2', form=form)
