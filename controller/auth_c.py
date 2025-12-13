# controller/auth_c.py
from typing import Optional
from db.connection import get_connection
from utils.security import hash_password, check_password
from models.usuario import Usuario


class AuthController:

    def registrar_usuario(self, usuario: Usuario) -> bool:
        if not usuario.clave:
            raise ValueError("La contraseña no puede ser None")

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO usuario
                (nombre_usuario, clave, nombre, apellido, fecha_nacimiento,
                 telefono, email, tipo)
                VALUES (:1, :2, :3, :4, :5, :6, :7, :8)
            """, (
                usuario.nombre_usuario,
                hash_password(usuario.clave),
                usuario.nombre,
                usuario.apellido,
                usuario.fecha_nacimiento,
                usuario.telefono,
                usuario.email,
                usuario.tipo
            ))

            conn.commit()
            return True

        except Exception as e:
            conn.rollback()
            print("Error registro:", e)
            return False

        finally:
            cursor.close()
            conn.close()

    def login(self, nombre_usuario: str, clave: str) -> Optional[Usuario]:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, nombre_usuario, clave, nombre, apellido, tipo
            FROM usuario
            WHERE nombre_usuario = :1
        """, (nombre_usuario,))

        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if not row:
            return None

        if not check_password(clave, row[2]):
            return None

        return Usuario(
            id=row[0],
            nombre_usuario=row[1],
            nombre=row[3],
            apellido=row[4],
            tipo=row[5]
        )
