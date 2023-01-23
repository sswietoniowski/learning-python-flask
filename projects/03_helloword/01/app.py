# 1st attempt to create a simple flask app
#
# At this stage everything (app) is in one file, after some time (with more routes) this will be a problem,
# as this file becomes too big and hard to maintain. So we want to split it into multiple files.

from flask import Flask

app = Flask(__name__)


@app.get("/")
def home():
    return "Hello World!"


@app.get("/something")
def something():
    return "Something"


if __name__ == "__main__":
    app.run()
