#models/models_tareas.py
from extensions import db  # Importa la instancia db


class Tarea(db.Model):
    __tablename__ = 'tarea'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    pendiente = db.Column(db.Boolean, default=True)
    completado = db.Column(db.Boolean, default=False)
    cancelado = db.Column(db.Boolean, default=False)
    fecha_creacion = db.Column(db.String(10))
    fecha_limite = db.Column(db.String(10))

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "estado": {
                "pendiente": self.pendiente,
                "completado": self.completado,
                "cancelado": self.cancelado
            },
            "fecha_creacion": self.fecha_creacion,
            "fecha_limite": self.fecha_limite
        }