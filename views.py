from flask import Blueprint, request, jsonify

from models import Subscriber
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
    chat = message.get('chat')
    if text.startswith('/subscribe'):
        _, name, url = text.split(' ')
        subscriber = Subscriber(chat.get('id'))
        s = Subscription.subscribe(name, url, subscriber.id)
    return jsonify({})
