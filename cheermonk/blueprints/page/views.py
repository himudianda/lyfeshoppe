from flask import Blueprint, jsonify

page = Blueprint('page', __name__)


# curl -i -X GET http://localhost:8000
@page.route('/')
def home():
    return jsonify({"Success": True})
