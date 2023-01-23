# 3rd attempt
#
# This version was initialized with: https://startbootstrap.com/theme/freelancer

from flask import render_template
from app import create_app


app = create_app()


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/content")
def content():
    return render_template("content.html")
