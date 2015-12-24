from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
from flask_login import login_required
page = Blueprint('page', __name__, template_folder='templates')


@page.route('/')
def home():
    return render_template('page/home.jinja2')


@page.route('/faq')
def faq():
    return render_template('page/faq.jinja2')


@page.route('/terms')
def terms():
    return render_template('page/terms.jinja2')


@page.route('/privacy')
def privacy():
    return render_template('page/privacy.jinja2')


@page.route('/investors')
def investors():
    return render_template('page/investors.jinja2')
