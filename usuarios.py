usuarios = []
id = 1

def agregar_usuario(nombre, edad):
    global id
    usuarios.append({
        "id": id,
        "nombre": nombre,
        "edad": edad
    })
    id+=1

def listar_usuarios():
    return usuarios

def obtener_usuarioById(id):
    for u in usuarios:
        if u["id"] == id:
            return u
    return None

def editar_usuarioById(id, nuevo_nombre, nueva_edad):
    for u in usuarios:
        if u["id"] == id:
            u["nombre"] = nuevo_nombre
            u["edad"] = nueva_edad
            return True
    return False

def eliminar_usuario(id):
    global usuarios
    usuarios = [u for u in usuarios if u["id"] != id]

def obtener_mayores():
    return [u for u in usuarios if u["edad"] >= 18]