from flask import jsonify
from marshmallow import Schema, ValidationError, fields, validate


# Esquema para el registro del usuario
class UserSchema(Schema):
    nombre = fields.Str(required=True, validate=validate.Length(min=1))
    apellido = fields.Str(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))

# Esquema para el inicio de sesión
class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

# Función externa para validar los datos de usuario
def validate_user(data):
    schema = UserSchema()
    try:
        return schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
