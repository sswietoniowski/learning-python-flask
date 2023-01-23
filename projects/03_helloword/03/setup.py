# 3rd attempt
#
# TODO: describe what we are doing here

from app import create_app

app = create_app()


@app.get("/")
def home():
    return "Hello World!"
