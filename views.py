from flask import Blueprint

views = Blueprint('views', __name__)


@views.route('/')
def hello_world():
    return 'Hello World!'
