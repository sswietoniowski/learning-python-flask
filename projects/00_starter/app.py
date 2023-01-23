from flask import Flask
from flask import request
from flask import current_app
from flask import make_response
from flask import redirect
from flask import url_for
from flask import abort
from flask import render_template


app = Flask(__name__)


@app.route("/")
# @app.route('/')
def index(user=None):
    user_agent = request.headers.get("User-Agent")
    app_name = current_app.name

    return render_template(
        "index.html", user_agent=user_agent, app_name=app_name, user=user
    )


@app.route("/user/<name>")
def user(name):
    if name != "jdoe":
        abort(404)
    return f"<h1>Hello, {name}!</h1>"


@app.route("/bad")
def bad():
    return "<h1>Bad Request!</h1>", 400


@app.route("/redirect")
def redirect_to():
    return redirect("/")


if __name__ == "__main__":
    app.run()
