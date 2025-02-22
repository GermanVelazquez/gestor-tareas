#controles/controles_users.py
from datetime import timedelta

from flask import jsonify, make_response, request
from flask_jwt_extended import (JWTManager, create_access_token,
                                get_jwt_identity, jwt_required)
from sqlalchemy.orm import joinedload

from extensions import db
from models.models_metas import Meta
from models.models_user import User
from models.schemas import LoginSchema, UserSchema


def login():
    # Obtener los datos enviados
    data = request.get_json() or {}

    # Validar los datos de entrada usando Marshmallow
    login_schema = LoginSchema()
    try:
        login_data = login_schema.load(data)  # Esto valida y deserializa los datos
    except ValidationError as err:
        return jsonify(err.messages), 400  # Devolver errores de validación

    email = login_data["email"]
    password = login_data["password"]

    # Verificar si el usuario existe y si la contraseña es correcta
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):  # Verifica si la contraseña es correcta
        # Crear un token JWT
        access_token = create_access_token(identity= str(User.id))  # Asegúrate de convertir el id a string
        
        # Crear la respuesta y guardar el token en una cookie
        response = make_response(jsonify({
            "message": "Inicio de sesión exitoso",
            "access_token": access_token  # Incluir el token en la respuesta
        }), 200)
        response.set_cookie("access_token", access_token, httponly=True, secure=True, max_age=timedelta(hours=1))

        return response

    # Si las credenciales son incorrectas
    return jsonify({"message": "Credenciales inválidas"}), 401


def register():
    data = request.get_json() or {}
    print(data)
    # Validar los datos usando Marshmallow
    user_schema = UserSchema()
    try:
        # Validamos y deserializamos los datos
        user_data = user_schema.load(data)  # Esto valida y transforma los datos
    except ValidationError as err:
        # Si hay errores de validación, los devolvemos en la respuesta
        return jsonify(err.messages), 400

    nombre = user_data["nombre"]
    apellido = user_data["apellido"]
    email = user_data["email"]
    password = user_data["password"]

    # Verificar si el usuario ya existe
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "El email ya está en uso"}), 400

    # Crear el usuario con contraseña hasheada
    nuevo_usuario = User(
        nombre=nombre,
        apellido=apellido,
        email=email
    )
    nuevo_usuario.set_password(password)  # Hashear la contraseña

    # Agregar el usuario a la base de datos
    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({"message": "Usuario registrado exitosamente", "user": nuevo_usuario.to_dict()}), 201


@jwt_required()
def perfil():
    try:
        usuario_id = get_jwt_identity()  # Obtiene el ID del usuario desde el token JWT
        
        # Cargar el usuario con sus metas y tareas asociadas usando joinedload
        usuario = User.query.options(joinedload(User.metas).joinedload(Meta.tareas)).get(usuario_id)

        # Si el usuario no existe
        if not usuario:
            return jsonify({"message": "Usuario no encontrado"}), 404

        # Calcular el progreso de cada meta
        metas_progreso = []
        for meta in usuario.metas:
            tareas_completadas = sum(1 for tarea in meta.tareas if tarea.completado)
            total_tareas = len(meta.tareas)
            progreso = (tareas_completadas / total_tareas) * 100 if total_tareas > 0 else 0
            metas_progreso.append({
                "meta": meta.to_dict(),  # Devolver los detalles de la meta
                "progreso": progreso  # Progreso calculado
            })
        
        # Responder con los datos del usuario y el progreso de sus metas
        return jsonify({"usuario": usuario.to_dict(), "metas_progreso": metas_progreso})

    except Exception as e:
        # Captura el error y muestra un mensaje más específico
        return jsonify({"message": f"Hubo un error al procesar la solicitud: {str(e)}"}), 500





@jwt_required()
def obtener_metas_usuario():
    usuario_id = get_jwt_identity()  # Obtiene el usuario autenticado
    usuario = User.query.get(usuario_id)

    if not usuario:
        return jsonify({"message": "Usuario no encontrado"}), 404

    return jsonify({"mis_metas": [meta.to_dict() for meta in usuario.metas]}), 200


@jwt_required()
def logout():
    # Eliminar el token JWT de la cookie (esto "desconecta" al usuario)
    response = make_response(jsonify({"message": "Logout exitoso"}), 200)
    response.delete_cookie("access_token", httponly=True, secure=True)
    
    return response