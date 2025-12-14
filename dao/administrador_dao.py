# dao/administrador_dao.py
from db.connection import get_connection
from models.usuario import Usuario

class AdministradorDAO:

    def crear(self, admin: Usuario) -> bool:
        conn = cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO usuario (nombre_usuario, clave, nombre, apellido, tipo)
                VALUES (:1, :2, :3, :4, 'admin')
            """, [
                admin.nombre_usuario,
                admin.clave,
                admin.nombre,
                admin.apellido
            ])
            conn.commit()
            return True
        finally:
            if cur: cur.close()
            if conn: conn.close()

    def obtener_por_id(self, admin_id: int) -> Usuario | None:
        conn = cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM usuario WHERE id=:id AND tipo='admin'", {"id": admin_id})
            row = cur.fetchone()
            if row:
                return Usuario(*row)
            return None
        finally:
            if cur: cur.close()
            if conn: conn.close()

    def listar(self) -> list[Usuario]:
        conn = cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM usuario WHERE tipo='admin' ORDER BY id")
            rows = cur.fetchall()
            return [Usuario(*r) for r in rows]
        finally:
            if cur: cur.close()
            if conn: conn.close()

    def actualizar(self, admin: Usuario) -> bool:
        conn = cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                UPDATE usuario
                SET nombre_usuario=:1, nombre=:2, apellido=:3, clave=:4
                WHERE id=:5 AND tipo='admin'
            """, [
                admin.nombre_usuario,
                admin.nombre,
                admin.apellido,
                admin.clave,
                admin.id
            ])
            conn.commit()
            return True
        finally:
            if cur: cur.close()
            if conn: conn.close()

    def eliminar(self, admin_id: int) -> bool:
        conn = cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM usuario WHERE id=:id AND tipo='admin'", {"id": admin_id})
            conn.commit()
            return True
        finally:
            if cur: cur.close()
            if conn: conn.close()
