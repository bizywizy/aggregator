import os

from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

from views import views
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://aggregator_user:qwerty@localhost:5432/aggregator'
db.init_app(app)
app.register_blueprint(views)

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    app.run()
