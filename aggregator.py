import os

from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

from models import db
from views import views

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

token = os.environ.get('TOKEN')
app.register_blueprint(views, url_prefix='/' + token)

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    app.run()
