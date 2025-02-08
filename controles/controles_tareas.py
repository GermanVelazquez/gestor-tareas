from flask import jsonify, request

from extensions import db
from models.models_tareas import Tarea


def add_tarea():
    data = request.get_json() or {}

    nueva_tarea = Tarea(
        nombre=data["nombre"],
        descripcion=data.get("descripcion", ""),
        pendiente=data["estado"].get("pendiente", True),
        completado=data["estado"].get("completado", False),
        cancelado=data["estado"].get("cancelado", False),
        fecha_creacion="{}-{}-{}".format(
            data["fecha_creacion"]["año"],
            data["fecha_creacion"]["mes"],
            data["fecha_creacion"]["dia"]
        ),
        fecha_limite="{}-{}-{}".format(
            data["fecha_limite"]["año"],
            data["fecha_limite"]["mes"],
            data["fecha_limite"]["dia"]
        )
    )

    db.session.add(nueva_tarea)
    db.session.flush()  # 🚀 Forzar a SQLAlchemy a asignar el ID antes del commit
    print(f"ID asignado después de flush: {nueva_tarea.id}")  # Verifica el ID
    db.session.commit()

    return jsonify(nueva_tarea.to_dict()), 201


def update_tarea(id):
    data = request.get_json() or {}
    tarea = Tarea.query.get(id)

    if tarea:
        tarea.nombre = data.get("nombre", tarea.nombre)
        tarea.descripcion = data.get("descripcion", tarea.descripcion)
        tarea.pendiente = data["estado"].get("pendiente", tarea.pendiente)
        tarea.completado = data["estado"].get("completado", tarea.completado)
        tarea.cancelado = data["estado"].get("cancelado", tarea.cancelado)
        tarea.fecha_limite = "{}-{}-{}".format(
            data["fecha_limite"]["año"],
            data["fecha_limite"]["mes"],
            data["fecha_limite"]["dia"]
        )

        db.session.commit()
        return jsonify({"message": "Tarea actualizada", "tarea": tarea.to_dict()}), 200

    return jsonify({"message": "Tarea no encontrada"}), 404

def get_tarea(id):
    tarea = Tarea.query.get(id)
    if tarea:
        return jsonify(tarea.to_dict()), 200
    return jsonify({"message": "Tarea no encontrada"}), 404

def search_tarea():
    nombre = request.args.get("nombre", "")
    estado = request.args.get("estado", "")

    query = Tarea.query
    if nombre:
        query = query.filter(Tarea.nombre.ilike(f"%{nombre}%"))
    if estado in ["pendiente", "completado", "cancelado"]:
        query = query.filter(getattr(Tarea, estado) == True)

    resultados = query.all()

    if resultados:
        return jsonify([t.to_dict() for t in resultados]), 200
    else:
        return jsonify({"message": "No se encontraron tareas con esos criterios"}), 404
    
def delete_tarea(id):
    tarea = Tarea.query.get(id)
    if tarea:
        db.session.delete(tarea)
        db.session.commit()
        return jsonify({"message": "Tarea eliminada"}), 200
    return jsonify({"message": "Tarea no encontrada"}), 404