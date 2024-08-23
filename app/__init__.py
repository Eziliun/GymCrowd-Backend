from flask import Flask
import requests
import json

link = "https://gymcrowd-default-rtdb.firebaseio.com/"

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    from .routes import main
    app.register_blueprint(main)

    return app