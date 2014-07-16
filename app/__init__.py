from BreakfastSerial import Arduino
from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy

from door import Door


app = Flask(__name__)
app.config.from_object('app.config')
app.debug = True

login_manager = LoginManager(app)
login_manager.session_protection = "strong"

db = SQLAlchemy(app)

if not app.debug:
    board = Arduino()
    door = Door(board)


from app import views
