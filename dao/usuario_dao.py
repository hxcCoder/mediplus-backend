from models.usuario import Usuario
from db.connection import get_connection

class UsuarioDAO:
    def __init__(self):
        self.conn = get_connection()

    def crear(self, usuario: Usuario):
        cursor = self.conn.cursor()
        sql = """
            INSERT INTO usuario
            (nombre_usuario, clave, nombre, apellido, fecha_nacimiento,
            telefono, email, tipo)
            VALUES (:1, :2, :3, :4, :5, :6, :7, :8)
        """
        cursor.execute(sql, (
            usuario.nombre_usuario,
            usuario.clave,
            usuario.nombre,
            usuario.apellido,
            usuario.fecha_nacimiento,
            usuario.telefono,
            usuario.email,
            usuario.tipo
        ))
        self.conn.commit()
        cursor.close()

    def obtener_por_id(self, usuario_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM usuario WHERE id = :1",
            (usuario_id,)
        )
        fila = cursor.fetchone()
        cursor.close()

        if fila:
            return Usuario(*fila)
        return None

    def listar(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM usuario")
        filas = cursor.fetchall()
        cursor.close()

        return [Usuario(*fila) for fila in filas]
