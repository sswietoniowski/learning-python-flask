# 2nd attempt at a flask app
#
# we've moved the app creation to a separate package

from app import create_app

app = create_app()


@app.get("/")
def home():
    return "Hello World!"
