from flask import Blueprint, request, jsonify
from subscription import Subscription

views = Blueprint('views', __name__)


@views.route('/')
def hello_world():
    return 'Hello World!'


@views.route('/', methods=['POST'])
def receive_update():
    update = request.json
    message = update.get('message')
    text = message.get('text')
    if text.startswith('/subscribe'):
        _, name, url = text.split(' ')
        s = Subscription.subscribe(name, url)
    return jsonify({})
