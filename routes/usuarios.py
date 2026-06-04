from flask import Blueprint, request, jsonify
from services.usuarios import UsuarioService

usuarios_bp = Blueprint("usuarios", __name__)

usuario_service = UsuarioService()


# GET → obtener todos
@usuarios_bp.route("/usuarios", methods=["GET"])
def get_usuarios():
    """
    Obtener todos los usuarios
    ---
    responses:
        200:
            description: Lista de usuarios
    """
    usuarios = usuario_service.listar_usuarios()
    return jsonify(usuarios)


# GET → uno solo
@usuarios_bp.route("/usuarios/<int:id>", methods=["GET"])
def get_usuario(id):
    """
    Obtener un usuario por su id
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true

    responses:
      200:
        description: Usuario encontrado
      404:
        description: Usuario no encontrado
    """
    usuario = usuario_service.obtener_usuarioById(id)

    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify(usuario)


# POST → crear
@usuarios_bp.route("/usuarios", methods=["POST"])
def crear_usuario():
    """
    Crear un usuario
    ---
    parameters:
      - in: body
        name: usuario
        required: true
        schema:
          type: object
          properties:
            nombre:
              type: string
            edad:
              type: integer
            usuario:
              type: string

    responses:
      201:
        description: Usuario creado
      400:
        description: Datos inválidos
    """
    data = request.json

    if not data:
        return jsonify({"error": "No se enviaron datos"}), 400

    if "nombre" not in data or "edad" not in data or "usuario" not in data:
        return jsonify({"error": "Faltan campos"}), 400

    nombre = data["nombre"]
    edad = data["edad"]
    usuario = data["usuario"]

    error = usuario_service.validar_nombre(nombre)
    if error:
        return jsonify({"error": error}), 400

    error = usuario_service.validar_usuario(usuario)
    if error:
        return jsonify({"error": error}), 400

    error = usuario_service.validar_edad(edad)
    if error:
        return jsonify({"error": error}), 400

    if usuario_service.existe_usuario(usuario):
        return jsonify({"error": "Usuario ya existe"}), 400

    creado = usuario_service.agregar_usuario(
        nombre,
        edad,
        usuario
    )

    if not creado:
        return jsonify({"error": "Error al crear usuario"}), 500

    return jsonify({"mensaje": "Usuario creado"}), 201


# PUT → editar completo
@usuarios_bp.route("/usuarios/<int:id>", methods=["PUT"])
def editar_usuario(id):
    """
    Reemplazar usuario completo
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true

      - in: body
        name: usuario
        required: true
        schema:
          type: object
          properties:
            nombre:
              type: string
            edad:
              type: integer
            usuario:
              type: string

    responses:
      200:
        description: Usuario actualizado
      404:
        description: Usuario no encontrado
    """
    data = request.json

    if not data:
        return jsonify({"error": "No se enviaron datos"}), 400

    if "nombre" not in data or "edad" not in data or "usuario" not in data:
        return jsonify({"error": "Faltan campos"}), 400

    nombre = data["nombre"]
    edad = data["edad"]
    usuario = data["usuario"]

    error = usuario_service.validar_nombre(nombre)
    if error:
        return jsonify({"error": error}), 400

    error = usuario_service.validar_usuario(usuario)
    if error:
        return jsonify({"error": error}), 400

    error = usuario_service.validar_edad(edad)
    if error:
        return jsonify({"error": error}), 400

    if usuario_service.existe_usuario_en_edicion(usuario, id):
        return jsonify({"error": "Usuario ya existe"}), 400

    actualizado = usuario_service.editar_usuario(
        id,
        nombre,
        edad,
        usuario
    )

    if not actualizado:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify({"mensaje": "Usuario actualizado"}), 200


# PATCH → editar parcial
@usuarios_bp.route("/usuarios/<int:id>", methods=["PATCH"])
def actualizar_parcial(id):
    """
    Actualizar parcialmente un usuario
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true

      - in: body
        name: usuario
        required: true
        schema:
          type: object
          properties:
            nombre:
              type: string
            edad:
              type: integer
            usuario:
              type: string

    responses:
      200:
        description: Usuario actualizado parcialmente
      404:
        description: Usuario no encontrado
    """
    data = request.json

    if not data:
        return jsonify({"error": "No se enviaron datos"}), 400

    usuario = usuario_service.obtener_usuarioById(id)

    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    if "nombre" in data:
        error = usuario_service.validar_nombre(data["nombre"])

        if error:
            return jsonify({"error": error}), 400

        usuario["nombre"] = data["nombre"]

    if "edad" in data:
        error = usuario_service.validar_edad(data["edad"])

        if error:
            return jsonify({"error": error}), 400

        usuario["edad"] = data["edad"]

    if "usuario" in data:
        error = usuario_service.validar_usuario(data["usuario"])

        if error:
            return jsonify({"error": error}), 400

        if usuario_service.existe_usuario_en_edicion(
            data["usuario"],
            id
        ):
            return jsonify({"error": "Usuario ya existe"}), 400

        usuario["usuario"] = data["usuario"]

    actualizado = usuario_service.editar_usuario(
        id,
        usuario["nombre"],
        usuario["edad"],
        usuario["usuario"]
    )

    if not actualizado:
        return jsonify({"error": "No se pudo actualizar"}), 400

    return jsonify({
        "mensaje": "Usuario actualizado parcialmente"
    }), 200


# DELETE → eliminar
@usuarios_bp.route("/usuarios/<int:id>", methods=["DELETE"])
def borrar_usuario(id):
    """
    Eliminar usuario
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true

    responses:
      200:
        description: Usuario eliminado
      404:
        description: Usuario no encontrado
    """
    eliminado = usuario_service.eliminar_usuario(id)

    if not eliminado:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify({"mensaje": "Usuario eliminado"}), 200