# app.py
import os

from dotenv import load_dotenv
from flask import Flask

from config import Config
from extensions import db  # Importa la instancia db definida en extensions.py
from routes.meta import metas_blueprint
from routes.tarea import tareas_blueprint

app = Flask(__name__)

# Cargar las variables de entorno desde el archivo .env
load_dotenv()



# Configuración de la base de datos
app.config.from_object('config.Config')  # Cargar desde el archivo config.py
db.init_app(app)

# Registrar los Blueprints
app.register_blueprint(tareas_blueprint, url_prefix="/tareas")
app.register_blueprint(metas_blueprint, url_prefix="/metas")

