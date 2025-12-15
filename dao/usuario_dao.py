from typing import Optional, List
from models.usuario import Usuario
from db.connection import get_connection
from utils.security import check_password

class UsuarioDAO:
    """DAO para la entidad Usuario"""

    def crear(self, usuario: Usuario) -> bool:
        usuario.tipo = usuario.tipo.upper() if usuario.tipo else "PACIENTE"
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
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
                        "clave": usuario.clave,
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
            return False

    def obtener_por_id(self, usuario_id: int) -> Optional[Usuario]:
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT id, nombre_usuario, clave, nombre, apellido,
                               fecha_nacimiento, telefono, email, tipo
                        FROM USUARIO
                        WHERE id = :id
                    """, {"id": usuario_id})
                    row = cursor.fetchone()
                    if row:
                        usuario = Usuario(*row)
                        usuario.tipo = usuario.tipo.upper() if usuario.tipo else "PACIENTE"
                        return usuario
                    return None
        except Exception as e:
            print("Error al obtener usuario por ID:", e)
            return None

    def obtener_por_nombre_usuario(self, nombre_usuario: str) -> Optional[Usuario]:
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT id, nombre_usuario, clave, nombre, apellido,
                               fecha_nacimiento, telefono, email, tipo
                        FROM USUARIO
                        WHERE nombre_usuario = :nombre_usuario
                    """, {"nombre_usuario": nombre_usuario})
                    row = cursor.fetchone()
                    if row:
                        usuario = Usuario(*row)
                        usuario.tipo = usuario.tipo.upper() if usuario.tipo else "PACIENTE"
                        return usuario
                    return None
        except Exception as e:
            print("Error al obtener usuario por nombre:", e)
            return None

    def login(self, nombre_usuario: str, clave: str) -> Optional[Usuario]:
        usuario = self.obtener_por_nombre_usuario(nombre_usuario)
        if usuario and usuario.clave and check_password(clave, usuario.clave):
            return usuario
        return None

    def listar(self) -> List[Usuario]:
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT id, nombre_usuario, clave, nombre, apellido,
                               fecha_nacimiento, telefono, email, tipo
                        FROM USUARIO
                        ORDER BY id
                    """)
                    rows = cursor.fetchall()
                    usuarios = []
                    for row in rows:
                        u = Usuario(*row)
                        u.tipo = u.tipo.upper() if u.tipo else "PACIENTE"
                        usuarios.append(u)
                    return usuarios
        except Exception as e:
            print("Error al listar usuarios:", e)
            return []

    def actualizar(self, usuario: Usuario) -> bool:
        usuario.tipo = usuario.tipo.upper() if usuario.tipo else "PACIENTE"
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
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
            return False

    def eliminar(self, usuario_id: int) -> bool:
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM USUARIO WHERE id = :id", {"id": usuario_id})
                    conn.commit()
            return True
        except Exception as e:
            print("Error al eliminar usuario:", e)
            return False
