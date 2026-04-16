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

    data = request.json

    if not data:
        return jsonify({"error": "No se enviaron datos"}), 400

    resultado = usuario_service.crear_usuario(data)

    if isinstance(resultado, str):
        return jsonify({"error": resultado}), 400

    if not resultado:
        return jsonify({"error": "Error al crear usuario"}), 500

    return jsonify({"mensaje": "Usuario creado"}), 201

# PUT → editar completo
@app.route("/usuarios/<int:id>", methods=["PUT"])
def actualizar_usuario(id):

    data = request.json

    if not data:
        return jsonify({"error": "No se enviaron datos"}), 400

    resultado = usuario_service.actualizar_usuario(id, data)

    if resultado is None:
        return jsonify({"error": "Usuario no encontrado"}), 404

    if isinstance(resultado, str):
        return jsonify({"error": resultado}), 400

    if not resultado:
        return jsonify({"error": "Error al actualizar"}), 500

    return jsonify({"mensaje": "Usuario actualizado"}), 200

# PATCH → editar parcial
@app.route("/usuarios/<int:id>", methods=["PATCH"])
def actualizar_parcial(id):

    data = request.json

    if not data:
        return jsonify({"error": "No se enviaron datos"}), 400

    resultado = usuario_service.editar_usuario_parcial(id, data)

    if resultado is None:
        return jsonify({"error": "Usuario no encontrado"}), 404

    if isinstance(resultado, str):
        return jsonify({"error": resultado}), 400

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