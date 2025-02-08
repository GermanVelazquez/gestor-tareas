from flask import Blueprint

from metas_controles.metas import (add_meta, add_tarea_to_meta, delete_meta,
                                   get_meta, update_meta)
from tareas_controles.controles_tarea import (add_tarea, get_tarea,
                                              search_tarea, update_tarea)

# Blueprint para tareas
tarea_blueprint = Blueprint('tarea', __name__)
# Blueprint para metas
metas_blueprint = Blueprint('metas', __name__)

# ----- Rutas para Tareas -----
tarea_blueprint.route("/<int:id>", methods=["GET"])(get_tarea)
tarea_blueprint.route("/", methods=["POST"])(add_tarea)
tarea_blueprint.route("/<int:id>", methods=["PUT"])(update_tarea)
tarea_blueprint.route("/search", methods=["GET"])(search_tarea)

# ----- Rutas para Metas -----
metas_blueprint.route("/", methods=["POST"])(add_meta)
metas_blueprint.route("/<int:id>", methods=["GET"])(get_meta)
metas_blueprint.route("/<int:id>", methods=["PUT"])(update_meta)
metas_blueprint.route("/<int:id>", methods=["DELETE"])(delete_meta)
metas_blueprint.route("/<int:meta_id>/add_tarea", methods=["PUT"])(add_tarea_to_meta)