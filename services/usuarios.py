import json
import os

class UsuarioService:
    
    def __init__(self):
        self.usuarios = []
        self.ruta = "data/usuarios.json"
        self.id = 1

    #---------------- Funciones y CRUD ----------------#
    
    def cargar_usuarios(self):
        if os.path.exists(self.ruta):
            with open(self.ruta, "r") as f:
                self.usuarios = json.load(f)
        else:
            self.usuarios = []

        # calcular siguiente ID
        if self.usuarios:
            self.id = max(u["id"] for u in self.usuarios) + 1
        else:
            self.id = 1

    def guardar_usuarios(self):
        with open(self.ruta, "w") as f:
            json.dump(self.usuarios, f, indent=4)

    def agregar_usuario(self, nombre, edad, usuario):
        nuevo = {
            "id": self.next_id,
            "nombre": nombre,
            "edad": edad,
            "usuario": usuario
        }

        self.usuarios.append(nuevo)
        self.id+=1
        self.guardar_usuarios()

    def listar_usuarios(self):
        return self.usuarios

    def obtener_usuarioById(self, id):
        for u in self.usuarios:
            if u["id"] == id:
                return u
        return None

    def editar_usuarioById(self, id, nuevo_nombre, nueva_edad, nuevo_usuario):
        for u in self.usuarios:
            if u["id"] == id:
                u["nombre"] = nuevo_nombre
                u["edad"] = nueva_edad
                u["usuario"] = nuevo_usuario
                
                self.guardar_usuarios()
                return True
        return False

    def eliminar_usuario(self, id):
        inicial = len(self.usuarios)
        self.usuarios = [u for u in self.usuarios if u["id"] != id]
        if len(self.usuarios) < inicial:
            self.guardar_usuarios()
            return True

        return False

    def obtener_mayores(self):
        return [u for u in self.usuarios if u["edad"] >= 18]
    
    #---------------- Validaciones Backend ----------------#

    def existe_usuario(self, usuario):
        return any(u["usuario"] == usuario for u in self.usuarios)
    
    def existe_usuario_en_edicion(self, usuario, id):
        return any(u["usuario"] == usuario and u["id"] != id for u in self.usuarios)
    
    def validar_nombre(self, nombre):
        if not isinstance(nombre, str):
            return "Nombre debe ser texto"
        
        if nombre.strip() == "":
            return "Nombre vacío"
        
        return None
    
    def validar_usuario(self, usuario):
        if not isinstance(usuario, str):
            return "Usuario debe ser texto"
        
        if usuario.strip() == "":
            return "Usuario vacío"
        
        return None
    
    def validar_edad(self, edad):
        if not isinstance(edad, int):
            return "Edad debe ser número"
        
        if edad < 0:
            return "Edad inválida"
        
        return None