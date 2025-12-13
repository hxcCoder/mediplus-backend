from models.usuario import Usuario
from db.connection import get_connection


class UsuarioDAO:

    @staticmethod
    def crear(usuario: Usuario):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
        INSERT INTO usuario (
            nombre_usuario, clave, nombre, apellido,
            fecha_nacimiento, telefono, email, tipo
        ) VALUES (
            :nombre_usuario, :clave, :nombre, :apellido,
            :fecha_nacimiento, :telefono, :email, :tipo
        )
        """

        cursor.execute(sql, {
            "nombre_usuario": usuario.nombre_usuario,
            "clave": usuario.clave,
            "nombre": usuario.nombre,
            "apellido": usuario.apellido,
            "fecha_nacimiento": usuario.fecha_nacimiento,
            "telefono": usuario.telefono,
            "email": usuario.email,
            "tipo": usuario.tipo
        })

        conn.commit()
        cursor.close()
        conn.close()

    # ------------------------------

    @staticmethod
    def obtener_por_nombre_usuario(nombre_usuario):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
        SELECT id, nombre_usuario, clave, nombre, apellido,
               fecha_nacimiento, telefono, email, tipo
        FROM usuario
        WHERE nombre_usuario = :nombre_usuario
        """

        cursor.execute(sql, {"nombre_usuario": nombre_usuario})
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row:
            return Usuario(*row)
        return None

    # ------------------------------

    @staticmethod
    def obtener_por_id(usuario_id):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
        SELECT id, nombre_usuario, clave, nombre, apellido,
               fecha_nacimiento, telefono, email, tipo
        FROM usuario
        WHERE id = :id
        """

        cursor.execute(sql, {"id": usuario_id})
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row:
            return Usuario(*row)
        return None

    # ------------------------------

    @staticmethod
    def actualizar(usuario: Usuario):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
        UPDATE usuario
        SET nombre = :nombre,
            apellido = :apellido,
            telefono = :telefono,
            email = :email
        WHERE id = :id
        """

        cursor.execute(sql, {
            "nombre": usuario.nombre,
            "apellido": usuario.apellido,
            "telefono": usuario.telefono,
            "email": usuario.email,
            "id": usuario.id
        })

        conn.commit()
        cursor.close()
        conn.close()

    # ------------------------------

    @staticmethod
    def eliminar(usuario_id):
        conn = get_connection()
        cursor = conn.cursor()

        sql = "DELETE FROM usuario WHERE id = :id"
        cursor.execute(sql, {"id": usuario_id})

        conn.commit()
        cursor.close()
        conn.close()
