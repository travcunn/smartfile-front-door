from flask import Blueprint, redirect, render_template, url_for
from flask.ext.login import login_required

from app import app
try:
    from app import door
except ImportError:
    class Door(object):
        def __init__(self):
            pass
        def unlock(self):
            pass
    door = Door()


mod = Blueprint('home', __name__)


@mod.route('/')
@login_required
def home():
    return render_template('home.html')


@mod.route('/unlock', methods=['POST'])
@login_required
def unlock():
    if not app.debug:
        door.unlock()
    return redirect(url_for('home.home'))
