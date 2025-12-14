from typing import Optional, List
from models.usuario import Usuario
from db.connection import get_connection
from utils.security import check_password


class UsuarioDAO:

    def crear(self, usuario: Usuario) -> bool:
        """Crea un nuevo usuario en la BD"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
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
                "clave": usuario.clave,  # YA VIENE HASHEADA
                "nombre": usuario.nombre,
                "apellido": usuario.apellido,
                "fecha_nacimiento": usuario.fecha_nacimiento,
                "telefono": usuario.telefono,
                "email": usuario.email,
                "tipo": usuario.tipo
            })
            conn.commit()
            return True
        except Exception as e:
            print("Error al crear usuario:", e)
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def obtener_por_id(self, usuario_id: int) -> Optional[Usuario]:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT id, nombre_usuario, clave, nombre, apellido,
                       fecha_nacimiento, telefono, email, tipo
                FROM usuario
                WHERE id = :id
            """, {"id": usuario_id})
            row = cursor.fetchone()
            if row:
                return Usuario(*row)
            return None
        finally:
            cursor.close()
            conn.close()

    def obtener_por_nombre_usuario(self, nombre_usuario: str) -> Optional[Usuario]:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT id, nombre_usuario, clave, nombre, apellido,
                       fecha_nacimiento, telefono, email, tipo
                FROM usuario
                WHERE nombre_usuario = :nombre_usuario
            """, {"nombre_usuario": nombre_usuario})
            row = cursor.fetchone()
            if row:
                return Usuario(*row)
            return None
        finally:
            cursor.close()
            conn.close()

    def login(self, nombre_usuario: str, clave: str) -> Optional[Usuario]:
        """
        Autenticación segura:
        - Busca usuario
        - Verifica hash de contraseña
        """
        usuario = self.obtener_por_nombre_usuario(nombre_usuario)
        if usuario and check_password(clave, usuario.clave):
            return usuario
        return None

    def listar(self) -> List[Usuario]:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT id, nombre_usuario, clave, nombre, apellido,
                       fecha_nacimiento, telefono, email, tipo
                FROM usuario
                ORDER BY id
            """)
            rows = cursor.fetchall()
            return [Usuario(*r) for r in rows]
        finally:
            cursor.close()
            conn.close()

    def actualizar(self, usuario: Usuario) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            sql = """
            UPDATE usuario
            SET nombre_usuario=:nombre_usuario,
                nombre=:nombre,
                apellido=:apellido,
                telefono=:telefono,
                email=:email,
                tipo=:tipo
            WHERE id=:id
            """
            cursor.execute(sql, {
                "nombre_usuario": usuario.nombre_usuario,
                "nombre": usuario.nombre,
                "apellido": usuario.apellido,
                "telefono": usuario.telefono,
                "email": usuario.email,
                "tipo": usuario.tipo,
                "id": usuario.id
            })
            conn.commit()
            return True
        except Exception as e:
            print("Error al actualizar usuario:", e)
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def eliminar(self, usuario_id: int) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM usuario WHERE id = :id",
                {"id": usuario_id}
            )
            conn.commit()
            return True
        except Exception as e:
            print("Error al eliminar usuario:", e)
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()
