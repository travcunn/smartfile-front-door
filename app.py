from BreakfastSerial import Arduino
from flask import Flask, redirect, url_for

from door import Door

app = Flask(__name__)
board = Arduino()
door = Door(board)


@app.route('/')
def home():
    return "<h1><a href='/unlock'>Unlock</a></h1>"


@app.route('/unlock')
def unlock():
    door.unlock()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(host='0.0.0.0')
