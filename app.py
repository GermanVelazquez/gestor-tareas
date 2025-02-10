# app.py
import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import Config
from extensions import db  # Importa la instancia db definida en extensions.py
from routes.meta import metas_blueprint
from routes.tarea import tareas_blueprint
from routes.users import users_blueprint

app = Flask(__name__)

# Cargar las variables de entorno desde el archivo .env
load_dotenv()
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")  #  Obtiene la clave segura del .env

CORS(app, supports_credentials=True)
# Inicializar JWTManager con la configuración de la app
jwt = JWTManager(app)

CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})  # Permite solicitudes desde el frontend
# Configuración de la base de datos
app.config.from_object('config.Config')  # Cargar desde el archivo config.py
db.init_app(app)

# Registrar los Blueprints
app.register_blueprint(tareas_blueprint, url_prefix="/tareas")
app.register_blueprint(metas_blueprint, url_prefix="/metas")
app.register_blueprint(users_blueprint, url_prefix="/users")