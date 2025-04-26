from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from passlib.context import CryptContext
from sqlalchemy import text

# Cargar variables de entorno
load_dotenv()

# Importar modelos y rutas
from models import db
from api import api

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Configuración
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+pymysql://api_user:StrongPassword123!@tu-endpoint-rds.rds.amazonaws.com/user_api')
    app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY', 'tu-secreto-super-seguro')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)

    # Inicializar extensiones
    db.init_app(app)
    jwt = JWTManager(app)

    # Registrar blueprints
    app.register_blueprint(api, url_prefix='/api')

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
