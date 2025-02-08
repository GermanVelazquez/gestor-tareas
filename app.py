# app.py
from flask import Flask
from extensions import db  # Importa la instancia db definida en extensions.py
from rutas.rutas import tarea_blueprint,metas_blueprint # Importa los Blueprints definidos en routes.py

app = Flask(__name__)

# Configuración de la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost:3306/flask_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)  # Inicializa SQLAlchemy con la aplicación

# Registrar los Blueprints para agrupar las rutas
app.register_blueprint(tarea_blueprint, url_prefix="/tareas")
app.register_blueprint(metas_blueprint, url_prefix="/metas")

# Crear todas las tablas en la base de datos si no existen
with app.app_context():
    db.create_all()