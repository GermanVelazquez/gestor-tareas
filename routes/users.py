#routes/users.py

from flask import Blueprint

from controles.controles_users import (login, logout, obtener_metas_usuario,
                                       perfil, register)

# Crear el Blueprint para usuarios
users_blueprint = Blueprint('user', __name__)  # Se llama 'user' al Blueprint

# ----- Rutas para el Usuario -----
users_blueprint.add_url_rule("/login", methods=["POST"], view_func=login)  # Ruta para login
users_blueprint.add_url_rule("/register", methods=["POST"], view_func=register)  # Ruta para registro  
users_blueprint.add_url_rule("/perfil", methods=["GET"], view_func=perfil)  # Ruta para obtener perfil
users_blueprint.add_url_rule("/logout", methods=["POST"], view_func=logout)  # Ruta para logout
users_blueprint.add_url_rule("/mis_metas", methods=["GET"], view_func=obtener_metas_usuario)  # Ruta para obtener metas del usuario
