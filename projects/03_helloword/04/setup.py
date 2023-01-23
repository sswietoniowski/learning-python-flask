# 4th attempt
#
# Now we are ready to make a better use of templates, by using the
# base.html template to render the index.html and content.html

from flask import render_template
from app import create_app


app = create_app()


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/content")
def content():
    return render_template("content.html")
