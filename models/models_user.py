from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from extensions import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)  # Asegura que el email sea único
    password = db.Column(db.String(255), nullable=False)  # Columna 'password' en la base de datos
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        """Encripta la contraseña antes de guardarla en la base de datos."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Verifica si la contraseña ingresada es correcta."""
        return check_password_hash(self.password, password)

    def to_dict(self):
        """Convierte el usuario a un diccionario, sin incluir la contraseña."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email
        }