from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

from views import views

app = Flask(__name__)

app.register_blueprint(views)

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    app.run()
