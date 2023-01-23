# 2nd attempt at a flask app, we're move the app creation to a separate package

from app_package import create_app

app = create_app()


@app.get("/")
def home():
    return "Hello World!"
