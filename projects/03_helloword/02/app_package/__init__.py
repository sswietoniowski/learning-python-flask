from flask import Flask


def create_app():
    """
    Initialize the Flask app instance
    """
    app = Flask(__name__)

    return app
