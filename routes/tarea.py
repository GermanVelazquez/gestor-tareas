#routes/tarea.py
from flask import Blueprint

from Controles.controles_tareas import (add_tarea, delete_tarea, get_tarea,
                                        search_tarea, update_tarea)

tareas_blueprint = Blueprint('tarea', __name__)

# ----- Rutas para Tareas -----
tareas_blueprint.add_url_rule("/", methods=["POST"], view_func=add_tarea)
tareas_blueprint.add_url_rule("/<int:id>", methods=["GET"], view_func=get_tarea)
tareas_blueprint.add_url_rule("/<int:id>", methods=["PUT"], view_func=update_tarea)
tareas_blueprint.add_url_rule("/<int:id>", methods=["DELETE"], view_func=delete_tarea)