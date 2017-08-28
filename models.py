from core import db


class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(255))
    url = db.Column(db.VARCHAR(255))
    last_link = db.Column(db.VARCHAR(255))
    subscriber_id = db.Column(db.Integer, db.ForeignKey('subscriber.id'), nullable=True)

    def __init__(self, name, url, last_link, subscriber_id):
        self.name = name
        self.url = url
        self.last_link = last_link
        self.subscriber_id = subscriber_id


class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.VARCHAR(255))
    username = db.Column(db.VARCHAR(255), nullable=True)
    first_name = db.Column(db.VARCHAR(255), nullable=True)
    last_name = db.Column(db.VARCHAR(255), nullable=True)
    subscriptions = db.relationship('Subscription', backref='subscriber', lazy='dynamic')

    def __init__(self, chat_id, username=None, first_name=None, last_name=None):
        self.chat_id = chat_id
        db.session.add(self)
        db.session.commit()
