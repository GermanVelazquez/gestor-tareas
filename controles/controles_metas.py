from flask import jsonify, request

from extensions import db
from models.models_metas import Meta
from models.models_tareas import Tarea


def add_meta():
    data = request.get_json() or {}

    nueva_meta = Meta(
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
        ),
        meta_padre=data.get("meta_padre", None)
    )

    # Asociar tareas a la meta, si se enviaron IDs en "tareas"
    tareas_ids = data.get("tareas", [])
    for tarea_id in tareas_ids:
        tarea = Tarea.query.get(tarea_id)
        if tarea:
            nueva_meta.tareas.append(tarea)

    db.session.add(nueva_meta)
    db.session.commit()

    return jsonify(nueva_meta.to_dict()), 201

def get_meta(id):
    meta = Meta.query.get(id)
    if meta:
        return jsonify(meta.to_dict()), 200
    return jsonify({"message": "Meta no encontrada"}), 404

def update_meta(id):
    data = request.get_json() or {}
    meta = Meta.query.get(id)

    if meta:
        meta.nombre = data.get("nombre", meta.nombre)
        meta.descripcion = data.get("descripcion", meta.descripcion)
        meta.pendiente = data["estado"].get("pendiente", meta.pendiente)
        meta.completado = data["estado"].get("completado", meta.completado)
        meta.cancelado = data["estado"].get("cancelado", meta.cancelado)
        meta.fecha_limite = "{}-{}-{}".format(
            data["fecha_limite"]["año"],
            data["fecha_limite"]["mes"],
            data["fecha_limite"]["dia"]
        )
        meta.meta_padre = data.get("meta_padre", meta.meta_padre)

        db.session.commit()
        return jsonify({"message": "Meta actualizada", "meta": meta.to_dict()}), 200

    return jsonify({"message": "Meta no encontrada"}), 404

def add_tarea_to_meta(meta_id):
    data = request.get_json() or {}
    tarea_id = data.get("tarea_id")
    if not tarea_id:
        return jsonify({"message": "Debe enviar 'tarea_id' en el JSON"}), 400

    meta = Meta.query.get(meta_id)
    tarea = Tarea.query.get(tarea_id)

    if meta and tarea:
        if tarea not in meta.tareas:
            meta.tareas.append(tarea)
            db.session.commit()
            return jsonify({"message": "Tarea agregada a la meta", "meta": meta.to_dict()}), 200
    elif not meta:
        return jsonify({"message": "Meta no encontrada"}), 404
    elif not tarea:
        return jsonify({"message": "Tarea no encontrada"}), 404

def delete_meta(id):
    meta = Meta.query.get(id)
    if meta:
        db.session.delete(meta)
        db.session.commit()
        return jsonify({"message": "Meta eliminada"}), 200
    return jsonify({"message": "Meta no encontrada"}), 404
