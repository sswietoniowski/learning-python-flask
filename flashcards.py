from datetime import datetime

from flask import Flask

app = Flask(__name__)


@app.route("/")
def welcome():
    return "Welcome to my Flash Cards application!"


@app.route("/date")
def date():
    return f"This page was served at {datetime.now()}"


counter = 0


@app.route("/count_views")
def count_views():
    global counter
    counter += 1
    return f"This page was server {counter} times"
