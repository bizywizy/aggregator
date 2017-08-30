from flask import Blueprint, request, jsonify

from core import db
from models import Subscriber, Subscription as SubscriptionDomain

views = Blueprint('views', __name__)


class CommandNotValid(Exception):
    pass


@views.route('/')
def hello_world():
    return 'Hello World!'


@views.route('/', methods=['POST'])
def receive_update():
    update = request.json
    message = update.get('message')
    text = message.get('text')
    chat_id = message.get('chat', {}).get('id')
    command, args = parse_text(text)
    commands = {
        '/start': lambda: [start(Subscriber.get_or_create(chat_id))],
        '/subscribe': lambda: [subscribe(Subscriber.get_or_create(chat_id), name) for name in args],
        '/unsubscribe': lambda: [unsubscribe(Subscriber.get_or_create(chat_id), name) for name in args],
        '/my_subscriptions': lambda: own_subscription_list(Subscriber.get_or_create(chat_id)),
        '/subscriptions': lambda: all_subscription_list()
    }

    return jsonify({})


# commands
def start(chat_id, **kwargs):
    Subscriber(chat_id)
    return {'status': 'ok', 'response': 'created subscriber'}


def subscribe(subscriber, name):
    subscription = SubscriptionDomain.get_by_name(name)
    if not subscription:
        return {'status': 'error', 'response': 'not found subscription \'{}\''.format(name)}
    subscription.subscribers.append(subscriber)
    db.session.add(subscription)
    db.session.commit()
    return {'status': 'ok', 'response': 'subscribed to \'{}\''.format(name)}


def unsubscribe(subscriber, name):
    subscription = SubscriptionDomain.get_by_name(name)
    if not subscription:
        return {'status': 'error', 'response': 'not found subscription \'{}\''.format(name)}
    try:
        subscription.subscribers.remove(subscriber)
        db.session.add(subscription)
        db.session.commit()
    except ValueError:
        return {'status': 'error', 'response': 'you are not subscribed to \'{}\''.format(name)}
    return {'status': 'ok', 'response': 'unsubscribed to \'{}\''.format(name)}


def own_subscription_list(subscriber):
    subscriptions = subscriber.subscriptions.all()
    if not subscriptions:
        return {'status': 'error', 'response': 'you have no subscriptions yet'}
    return {'status': 'ok', 'response': {'subscriptions': [str(subscription) for subscription in subscriptions]}}


def all_subscription_list():
    subscriptions = SubscriptionDomain.query.all()
    if not subscriptions:
        return {'status': 'error', 'response': 'we have no subscriptions yet'}
    return {'status': 'ok', 'response': {'subscriptions': [str(subscription) for subscription in subscriptions]}}


# utils
def parse_text(text):
    commands = ('/start', '/subscribe', '/unsubscribe', '/my_subscriptions', '/subscriptions')
    command, *args = text.split()
    if command not in commands:
        raise CommandNotValid()
    return command, args
