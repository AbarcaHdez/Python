usuarios = [{"nombre": 'Juan', "edad": 25},{"nombre":'Sebastian',"edad": 23}]

def agregar_usuario(nombre, edad):
    usuarios.append({
        "nombre": nombre,
        "edad": edad
    })

def listar_usuarios():
    return usuarios

def obtener_usuarioByNombre(nombre):
    for u in usuarios:
        if u["nombre"] == nombre:
            return u
    return None

def editar_usuario(nombre, nueva_edad):
    for u in usuarios:
        if u["nombre"] == nombre:
            u["edad"] = nueva_edad
            return True
    return False

def eliminar_usuario(nombre):
    global usuarios
    usuarios = [u for u in usuarios if u["nombre"] != nombre]

def obtener_mayores():
    return [u for u in usuarios if u["edad"] >= 18]

print(editar_usuario("Juan", 26))

print(usuarios)