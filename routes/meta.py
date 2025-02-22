#routes/meta.py
from flask import Blueprint

from controles.controles_metas import (add_meta, add_tarea_to_meta,
                                       delete_meta, get_meta, update_meta)

metas_blueprint = Blueprint('metas', __name__)

# ----- Rutas para Metas -----
metas_blueprint.add_url_rule("/", methods=["POST"], view_func=add_meta)
metas_blueprint.add_url_rule("/<int:id>", methods=["GET"], view_func=get_meta)
metas_blueprint.add_url_rule("/<int:id>", methods=["PUT"], view_func=update_meta)
metas_blueprint.add_url_rule("/<int:id>", methods=["DELETE"], view_func=delete_meta)
metas_blueprint.add_url_rule("/<int:meta_id>/tareas", methods=["POST"], view_func=add_tarea_to_meta)
