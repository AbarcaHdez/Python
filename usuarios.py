import json
import os

usuarios = []
RUTA = "data/usuarios.json"
id = 1

def cargar_usuarios():
    global usuarios, id

    if os.path.exists(RUTA):
        with open(RUTA, "r") as f:
            usuarios = json.load(f)
    else:
        usuarios = []

    # calcular siguiente ID
    if usuarios:
        id = max(u["id"] for u in usuarios) + 1
    else:
        id = 1

def guardar_usuarios():
    with open(RUTA, "w") as f:
        json.dump(usuarios, f, indent=4)

def agregar_usuario(nombre, edad, usuario):
    global id
    usuarios.append({
        "id": id,
        "nombre": nombre,
        "edad": edad,
        "usuario" : usuario
    })
    id+=1
    guardar_usuarios()

def listar_usuarios():
    return usuarios

def obtener_usuarioById(id):
    for u in usuarios:
        if u["id"] == id:
            return u
    return None

def editar_usuarioById(id, nuevo_nombre, nueva_edad, nuevo_usuario):
    for u in usuarios:
        if u["id"] == id:
            u["nombre"] = nuevo_nombre
            u["edad"] = nueva_edad
            u["usuario"] = nuevo_usuario
            
            guardar_usuarios()
            return True
    return False

def eliminar_usuario(id):
    global usuarios

    inicial = len(usuarios)

    usuarios = [u for u in usuarios if u["id"] != id]

    if len(usuarios) < inicial:
        guardar_usuarios()
        return True

    return False

def obtener_mayores():
    return [u for u in usuarios if u["edad"] >= 18]