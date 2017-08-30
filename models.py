from core import db

subscriptions = db.Table('subscriptions',
                         db.Column('subscription_id', db.Integer, db.ForeignKey('subscription.id')),
                         db.Column('subscriber', db.Integer, db.ForeignKey('subscriber.id'))
                         )


class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(255), unique=True)
    url = db.Column(db.VARCHAR(255))
    last_link = db.Column(db.VARCHAR(255), nullable=True)
    subscribers = db.relationship('Subscriber', secondary=subscriptions,
                                  backref=db.backref('subscriptions', lazy='dynamic'))

    def __init__(self, name, url):
        self.name = name
        self.url = url

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def __str__(self):
        return self.name


class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.VARCHAR(255), unique=True)
    username = db.Column(db.VARCHAR(255), nullable=True)
    first_name = db.Column(db.VARCHAR(255), nullable=True)
    last_name = db.Column(db.VARCHAR(255), nullable=True)
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscription.id'), nullable=True)

    def __init__(self, chat_id, username=None, first_name=None, last_name=None):
        self.chat_id = chat_id
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_or_create(cls, chat_id, **kwargs):
        subscriber = cls.query.filter_by(chat_id).first()
        if subscriber:
            return subscriber, False
        else:
            subscriber = cls(chat_id)
            db.session.add(subscriber)
            db.session.commit()
            return subscriber, True
