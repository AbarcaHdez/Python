import sqlite3

class UsuarioService:

    def __init__(self):
        self.conn = sqlite3.connect("data/usuarios.db", check_same_thread=False)
        self.conn.row_factory = sqlite3.Row 
        self.cursor = self.conn.cursor()
        self.crear_tabla()

    # ---------------- CRUD ---------------- #

    def agregar_usuario(self, nombre, edad, usuario):
        try:
            self.cursor.execute(
                "INSERT INTO usuarios (nombre, edad, usuario) VALUES (?, ?, ?)",
                (nombre, edad, usuario)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def listar_usuarios(self):
        self.cursor.execute("SELECT * FROM usuarios")
        filas = self.cursor.fetchall()
        return [dict(f) for f in filas]

    def obtener_usuarioById(self, id):
        self.cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id,))
        fila = self.cursor.fetchone()
        return dict(fila) if fila else None
    
    def eliminar_usuario(self, id):
        self.cursor.execute("DELETE FROM usuarios WHERE id = ?", (id,))
        self.conn.commit()
        return self.cursor.rowcount > 0

    # ---------------- Preparar Validaciones ---------------- #

    def editar_usuario(self, id, nombre, edad, usuario):
        self.cursor.execute(
            "UPDATE usuarios SET nombre = ?, edad = ?, usuario = ? WHERE id = ?",
            (nombre, edad, usuario, id)
        )
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def crear_usuario(self, data):
        # validar campos obligatorios
        if "nombre" not in data or "edad" not in data or "usuario" not in data:
            return "Faltan campos: nombre, edad, usuario"

        nombre = data["nombre"]
        edad = data["edad"]
        usuario = data["usuario"]

        # validaciones
        error = self.validar_nombre(nombre)
        if error:
            return error

        error = self.validar_usuario(usuario)
        if error:
            return error

        error = self.validar_edad(edad)
        if error:
            return error

        if self.existe_usuario(usuario):
            return "Usuario ya existe"

        # guardar
        creado = self.agregar_usuario(nombre, edad, usuario)

        return creado
    
    def actualizar_usuario(self, id, data):

        usuario = self.obtener_usuarioById(id)

        if not usuario:
            return None  # no existe

        # validar campos obligatorios
        if "nombre" not in data or "edad" not in data or "usuario" not in data:
            return "Faltan campos: nombre, edad, usuario"

        nombre = data["nombre"]
        edad = data["edad"]
        usuario_nombre = data["usuario"]

        # validaciones
        error = self.validar_nombre(nombre)
        if error:
            return error

        error = self.validar_usuario(usuario_nombre)
        if error:
            return error

        error = self.validar_edad(edad)
        if error:
            return error

        if self.existe_usuario_en_edicion(usuario_nombre, id):
            return "Usuario ya existe"

        actualizado = self.editar_usuario(id, nombre, edad, usuario_nombre)

        return actualizado
    
    def editar_usuario_parcial(self, id, data):
        usuario = self.obtener_usuarioById(id)

        if not usuario:
            return None  # no existe

        # valores actuales
        nombre = usuario["nombre"]
        edad = usuario["edad"]
        usuario_nombre = usuario["usuario"]

        # actualizar solo lo que venga
        if "nombre" in data:
            if not isinstance(data["nombre"], str) or data["nombre"].strip() == "":
                return "Nombre inválido"
            nombre = data["nombre"]

        if "edad" in data:
            if not isinstance(data["edad"], int) or data["edad"] < 0:
                return "Edad inválida"
            edad = data["edad"]

        if "usuario" in data:
            if not isinstance(data["usuario"], str) or data["usuario"].strip() == "":
                return "Usuario inválido"

            if self.existe_usuario_en_edicion(data["usuario"], id):
                return "Usuario ya existe"

            usuario_nombre = data["usuario"]

        # guardar cambios
        actualizado = self.editar_usuario(id, nombre, edad, usuario_nombre)

        return actualizado

    
    # ---------------- Validaciones ---------------- #

    def existe_usuario(self, usuario):
        self.cursor.execute(
            "SELECT 1 FROM usuarios WHERE usuario = ?", (usuario,)
        )
        return self.cursor.fetchone() is not None

    def existe_usuario_en_edicion(self, usuario, id):
        self.cursor.execute(
            "SELECT 1 FROM usuarios WHERE usuario = ? AND id != ?",
            (usuario, id)
        )
        return self.cursor.fetchone() is not None

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

    # ---------------- Base de Datos ---------------- #

    def crear_tabla(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                edad INTEGER NOT NULL,
                usuario TEXT UNIQUE NOT NULL
            )
        """)
        self.conn.commit()