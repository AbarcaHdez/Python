from services.usuarios import UsuarioService
from flask import Flask, request, jsonify
from flasgger import Swagger
from services.usuarios import *

usuario_service = UsuarioService()

app = Flask(__name__)
swagger = Swagger(app)

# GET → obtener todos
@app.route("/usuarios", methods=["GET"])
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
@app.route("/usuarios/<int:id>", methods=["GET"])
def get_usuario(id):
    """
    Obtener un usuario por su id
    ---
    responses:
        200:
            description: Lista un usuario
    """
    usuario = usuario_service.obtener_usuarioById(id)

    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify(usuario)

# POST → crear
@app.route("/usuarios", methods=["POST"])
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

    # Validaciones
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

    creado = usuario_service.agregar_usuario(nombre, edad, usuario)

    if not creado:
        return jsonify({"error": "Error al crear usuario"}), 500

    return jsonify({"mensaje": "Usuario creado"}), 201

# PUT → editar completo
@app.route("/usuarios/<int:id>", methods=["PUT"])
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

    nombre = data["nombre"]
    edad = data["edad"]
    usuario = data["usuario"]

    if usuario_service.existe_usuario_en_edicion(usuario, id):
        return jsonify({"error": "Usuario ya existe"}), 400

    actualizado = usuario_service.editar_usuario(id, nombre, edad, usuario)

    if not actualizado:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify({"mensaje": "Usuario actualizado"}), 200

# PATCH → editar parcial
@app.route("/usuarios/<int:id>", methods=["PATCH"])
def actualizar_parcial(id):
    """
    Actualizar parcialmente un usuario
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID del usuario

      - in: body
        name: usuario
        required: true
        schema:
          type: object
          properties:
            nombre:
              type: string
              example: Juan
            edad:
              type: integer
              example: 30
            usuario:
              type: string
              example: juan123

    responses:
      200:
        description: Permite actualizar uno o más campos del usuario sin necesidad de enviar todos.
      400:
        description: Datos inválidos
      404:
        description: Usuario no encontrado
    """
    data = request.json

    if not data:
        return jsonify({"error": "No se enviaron datos"}), 400

    usuario = usuario_service.obtener_usuarioById(id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    # Validaciones (solo si vienen)
    if "nombre" in data:
        if not isinstance(data["nombre"], str) or data["nombre"].strip() == "":
            return jsonify({"error": "Nombre inválido"}), 400
        usuario["nombre"] = data["nombre"]

    if "edad" in data:
        if not isinstance(data["edad"], int) or data["edad"] < 0:
            return jsonify({"error": "Edad inválida"}), 400
        usuario["edad"] = data["edad"]

    if "usuario" in data:
        if not isinstance(data["usuario"], str) or data["usuario"].strip() == "":
            return jsonify({"error": "Usuario inválido"}), 400

        if any(u["usuario"] == data["usuario"] and u["id"] != id for u in usuario_service.usuarios):
            return jsonify({"error": "Usuario ya existe"}), 400

        usuario["usuario"] = data["usuario"]

    return jsonify({"mensaje": "Usuario actualizado parcialmente"}), 200

# DELETE → eliminar
@app.route("/usuarios/<int:id>", methods=["DELETE"])
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

if __name__ == "__main__":
    app.run(debug=True)