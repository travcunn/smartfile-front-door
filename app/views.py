from flask import g
from flask.ext.login import current_user

from app import app, login_manager
from app.auth.views import mod as auth_module
from app.home.views import mod as home_module
from app.models import User

login_manager.login_view = 'auth.login'
login_manager.login_message = ""


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user


app.register_blueprint(auth_module)
app.register_blueprint(home_module)
