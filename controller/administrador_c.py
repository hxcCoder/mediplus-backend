from db.connection import get_connection
from models.usuario import Usuario

class AdministradorController:

    # Crear administrador
    def crear(self, admin: Usuario):
        conn = cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            sql = """
                INSERT INTO usuario (nombre_usuario, clave, nombre, apellido, tipo)
                VALUES (:1, :2, :3, :4, :5)
            """
            cur.execute(sql, [
                admin.nombre_usuario,
                admin.clave,
                admin.nombre,
                admin.apellido,
                "admin"
            ])
            conn.commit()
            return True
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    # Obtener administrador por ID
    def obtener_por_id(self, admin_id):
        conn = cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            sql = "SELECT * FROM usuario WHERE id = :id AND tipo = 'admin'"
            cur.execute(sql, {"id": admin_id})
            row = cur.fetchone()
            if row:
                return Usuario(*row)
            return None
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    # Listar todos los administradores
    def listar(self):
        conn = cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM usuario WHERE tipo = 'admin' ORDER BY id")
            rows = cur.fetchall()
            return [Usuario(*r) for r in rows]
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    # Actualizar administrador
    def actualizar(self, admin: Usuario):
        conn = cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            sql = """
                UPDATE usuario
                SET nombre_usuario=:1, nombre=:2, apellido=:3, clave=:4
                WHERE id=:5 AND tipo='admin'
            """
            cur.execute(sql, [
                admin.nombre_usuario,
                admin.nombre,
                admin.apellido,
                admin.clave,
                admin.id
            ])
            conn.commit()
            return True
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    # Eliminar administrador
    def eliminar(self, admin_id):
        conn = cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM usuario WHERE id=:id AND tipo='admin'", {"id": admin_id})
            conn.commit()
            return True
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
