from typing import Optional, List
from models.usuario import Usuario
from db.connection import get_connection
from utils.security import check_password


class UsuarioDAO:
    """DAO para la entidad Usuario"""

    def crear(self, usuario: Usuario) -> bool:
        """Crea un nuevo usuario en la base de datos"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            sql = """
            INSERT INTO USUARIO (
                nombre_usuario, clave, nombre, apellido,
                fecha_nacimiento, telefono, email, tipo
            ) VALUES (
                :nombre_usuario, :clave, :nombre, :apellido,
                :fecha_nacimiento, :telefono, :email, :tipo
            )
            """
            cursor.execute(sql, {
                "nombre_usuario": usuario.nombre_usuario,
                "clave": usuario.clave,  # contraseña hasheada
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
        """Obtiene un usuario por su ID"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT id, nombre_usuario, clave, nombre, apellido,
                    fecha_nacimiento, telefono, email, tipo
                FROM USUARIO
                WHERE id = :id
            """, {"id": usuario_id})
            row = cursor.fetchone()
            return Usuario(*row) if row else None
        finally:
            cursor.close()
            conn.close()

    def obtener_por_nombre_usuario(self, nombre_usuario: str) -> Optional[Usuario]:
        """Obtiene un usuario por su nombre de usuario"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT id, nombre_usuario, clave, nombre, apellido,
                    fecha_nacimiento, telefono, email, tipo
                FROM USUARIO
                WHERE nombre_usuario = :nombre_usuario
            """, {"nombre_usuario": nombre_usuario})
            row = cursor.fetchone()
            return Usuario(*row) if row else None
        finally:
            cursor.close()
            conn.close()

    def login(self, nombre_usuario: str, clave: str) -> Optional[Usuario]:
        """Autenticación segura de usuario"""
        usuario = self.obtener_por_nombre_usuario(nombre_usuario)
        if usuario and check_password(clave, usuario.clave):
            return usuario
        return None

    def listar(self) -> List[Usuario]:
        """Lista todos los usuarios"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT id, nombre_usuario, clave, nombre, apellido,
                    fecha_nacimiento, telefono, email, tipo
                FROM USUARIO
                ORDER BY id
            """)
            rows = cursor.fetchall()
            return [Usuario(*row) for row in rows]
        finally:
            cursor.close()
            conn.close()

    def actualizar(self, usuario: Usuario) -> bool:
        """Actualiza los datos de un usuario"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            sql = """
            UPDATE USUARIO
            SET nombre_usuario = :nombre_usuario,
                nombre = :nombre,
                apellido = :apellido,
                telefono = :telefono,
                email = :email,
                tipo = :tipo
            WHERE id = :id
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
        """Elimina un usuario por su ID"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM USUARIO WHERE id = :id",
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
