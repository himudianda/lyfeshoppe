from flask import Blueprint, render_template

sample = Blueprint('sample', __name__, template_folder='templates')


@sample.route('/')
def index():
    return render_template('sample/index.html')


@sample.route('/')
def app_calendar():
    return render_template('sample/app_calendar.html')
