from functools import wraps
import hashlib
import os

from BreakfastSerial import Arduino
from flask import Flask, jsonify,  redirect, render_template, \
    request, Response, url_for

from door import Door


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
board = Arduino()
door = Door(board)

USERS = {'travis': 'df37decdae20af5da3335d5b574025bd3a79cc617f5ba274103928bda2a24fb6',
         'alex': 'dd1acf1e3d5f020ac0b3bf791910ea76bb4e86c39ef2840541d5c903d2468b69'}


def check_auth(username, password):
    hasher = hashlib.sha256()
    hasher.update(password)
    password = hasher.hexdigest()

    authenticated = False
    correct_pass = USERS.get(username)
    if correct_pass is not None:
        if correct_pass == password:
            authenticated = True

    if authenticated:
        print("[Front Door]: User (%s) has unlocked the door" % username)

    return authenticated


def authenticate():
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/unlock', methods=['POST'])
@requires_auth
def unlock():
    door.unlock()
    return redirect(url_for('home'))


@app.route('/api/unlock', methods=['POST'])
@requires_auth
def api_unlock():
    door.unlock()

    json_data = {"ok": "success"}
    return jsonify(json_data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)
