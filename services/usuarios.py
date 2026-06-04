import sqlite3

class UsuarioService:

    def __init__(self):
        self.conn = sqlite3.connect(
            "data/usuarios.db",
            check_same_thread=False
        )
        self.cursor = self.conn.cursor()
        self.crear_tabla()

    # ---------------- Funciones y CRUD ---------------- #

    def agregar_usuario(self, nombre, edad, usuario):
        try:
            self.cursor.execute(
                "INSERT INTO usuarios (nombre, edad, usuario) VALUES (?, ?, ?)",
                (nombre, edad, usuario)
            )
            self.conn.commit()
            return True
        except:
            return False

    def listar_usuarios(self):
        self.cursor.execute("SELECT * FROM usuarios")
        filas = self.cursor.fetchall()
        return [self.formatear_usuario(f) for f in filas]

    def obtener_usuarioById(self, id):
        self.cursor.execute(
            "SELECT * FROM usuarios WHERE id = ?",
            (id,)
        )
        fila = self.cursor.fetchone()
        return self.formatear_usuario(fila)

    def editar_usuario(self, id, nombre, edad, usuario):
        self.cursor.execute(
            "UPDATE usuarios SET nombre = ?, edad = ?, usuario = ? WHERE id = ?",
            (nombre, edad, usuario, id)
        )
        self.conn.commit()
        return self.cursor.rowcount > 0

    def eliminar_usuario(self, id):
        self.cursor.execute(
            "DELETE FROM usuarios WHERE id = ?",
            (id,)
        )
        self.conn.commit()
        return self.cursor.rowcount > 0

    # ---------------- Validaciones Backend ---------------- #

    def existe_usuario(self, usuario):
        self.cursor.execute(
            "SELECT 1 FROM usuarios WHERE usuario = ?",
            (usuario,)
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

    def formatear_usuario(self, fila):
        if not fila:
            return None

        return {
            "id": fila[0],
            "nombre": fila[1],
            "edad": fila[2],
            "usuario": fila[3]
        }