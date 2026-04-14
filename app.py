from flask import Flask, request, jsonify
from usuarios import *

app = Flask(__name__)

# GET → obtener todos
@app.route("/usuarios", methods=["GET"])
def get_usuarios():
    return jsonify(listar_usuarios())

# GET → uno solo
@app.route("/usuarios/<int:id>", methods=["GET"])
def get_usuario(id):
    usuario = obtener_usuarioById(id)
    if usuario:
        return jsonify(usuario)
    return jsonify({"error": "Usuario no encontrado"}), 404

# POST → crear
@app.route("/usuarios", methods=["POST"])
def crear_usuario():
    data = request.json
    agregar_usuario(data["nombre"], data["edad"])
    return jsonify({"mensaje": "Usuario agregado"}), 201

# POST → editar
@app.route("/usuarios/<int:id>", methods=["PUT"])
def editar_usuario(id):
    data = request.json
    if not data or "edad" not in data or "nombre" not in data:
        return jsonify({"error": "Datos inválidos"}), 400
    editar = editar_usuarioById(id,data["nombre"],data["edad"])
    if editar:
        return jsonify({"mensaje": "Usuario editado"}), 200
    return jsonify({"error": "Usuario no encontrado"}), 404

# DELETE → eliminar
@app.route("/usuarios/<int:id>", methods=["DELETE"])
def borrar_usuario(id):
    eliminar_usuario(id)
    return jsonify({"mensaje": "Usuario eliminado"})

if __name__ == "__main__":
    app.run(debug=True)