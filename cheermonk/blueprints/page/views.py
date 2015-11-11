from flask import Blueprint, render_template

page = Blueprint('page', __name__, template_folder='templates')


# curl -i -X GET http://localhost:5000
@page.route('/')
def home():
    return render_template('page/home.jinja2')
