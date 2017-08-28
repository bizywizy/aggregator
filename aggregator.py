import os

from werkzeug.contrib.fixers import ProxyFix

from core import app
from views import views

token = os.environ.get('TOKEN')
app.register_blueprint(views, url_prefix='/' + token)

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    app.run()
