from aggregator import db


class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(255))
    url = db.Column(db.VARCHAR(255))
    last_link = db.Column(db.VARCHAR(255))
    subscriber = db.Column(db.Integer, db.ForeignKey('subscriber.id'))

    def __init__(self, name, url, last_link):
        self.name = name
        self.url = url
        self.last_link = last_link


class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.VARCHAR(255))
    username = db.Column(db.VARCHAR(255), nullable=True)
    first_name = db.Column(db.VARCHAR(255), nullable=True)
    last_name = db.Column(db.VARCHAR(255), nullable=True)
    subscriptions = db.relationship('Subscription', backref='subscriber', lazy='dynamic')
