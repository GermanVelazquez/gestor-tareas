from extensions import db  # Importa la instancia db

class Tarea(db.Model):
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

class Meta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    pendiente = db.Column(db.Boolean, default=True)
    completado = db.Column(db.Boolean, default=False)
    cancelado = db.Column(db.Boolean, default=False)
    fecha_creacion = db.Column(db.String(10))
    fecha_limite = db.Column(db.String(10))
    meta_padre = db.Column(db.Integer, db.ForeignKey("meta.id"), nullable=True)
    # Relación many-to-many entre Meta y Tarea
    tareas = db.relationship("Tarea", secondary="meta_tarea", backref="metas")

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
            "fecha_limite": self.fecha_limite,
            "meta_padre": self.meta_padre,
            "tareas": [t.id for t in self.tareas]
        }

# Tabla de asociación para la relación many-to-many entre Meta y Tarea.
meta_tarea = db.Table(
    "meta_tarea",
    db.Column("meta_id", db.Integer, db.ForeignKey("meta.id"), primary_key=True),
    db.Column("tarea_id", db.Integer, db.ForeignKey("tarea.id"), primary_key=True)
)