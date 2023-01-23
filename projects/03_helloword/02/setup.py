# 2nd attempt at a flask app
#
# We've moved the app creation to a separate package
#
# More info about this idea here: https://flask.palletsprojects.com/en/2.2.x/patterns/appfactories/

from app import create_app

app = create_app()


@app.get("/")
def home():
    return "Hello World!"
