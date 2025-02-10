#config.py
import os

from dotenv import load_dotenv

load_dotenv()  # Cargar variables de entorno

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", False)
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")  # Obtener la clave secreta de JWT desde el .env