from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(255))
    url = db.Column(db.VARCHAR(255))
    last_link = db.Column(db.VARCHAR(255))

    def __init__(self, name, url, last_link):
        self.name = name
        self.url = url
        self.last_link = last_link
