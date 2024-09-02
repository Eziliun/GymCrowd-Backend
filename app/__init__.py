from flask import Flask
from .firebase_config import initialize_firebase

def create_app():
    app = Flask(__name__)
    
    # Configurações do Flask
    app.config.from_object('config')

    # Inicializar Firebase
    db = initialize_firebase()
    
    app.config['FIRESTORE_DB'] = db

    # Importa as rotas
    from .routes import auth_bp
    app.register_blueprint(auth_bp)

    return app
