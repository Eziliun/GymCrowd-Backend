from flask import Flask
from flask_cors import CORS
from .firebase_config import initialize_firebase

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})
    
    app.config.from_object('config')
    
    db = initialize_firebase()
    app.config['FIREBASE_DB'] = db

    from .routes import auth_bp
    app.register_blueprint(auth_bp)

    return app
