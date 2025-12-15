from typing import Optional
from models.usuario import Usuario
from dao.usuario_dao import UsuarioDAO
from utils.security import hash_password, check_password

class AuthController:
    def __init__(self, usuario_dao: Optional[UsuarioDAO] = None):
        self.usuario_dao = usuario_dao or UsuarioDAO()

    def registrar_usuario(self, usuario: Usuario) -> bool:
        if not usuario.nombre_usuario or not usuario.clave:
            return False
        # Evitar duplicados
        if self.usuario_dao.obtener_por_nombre_usuario(usuario.nombre_usuario):
            return False
        # Guardamos la contraseña hasheada
        usuario.clave = hash_password(usuario.clave)
        usuario.tipo = usuario.tipo.upper() if usuario.tipo else "PACIENTE"
        return self.usuario_dao.crear(usuario)

    def login(self, nombre_usuario: str, clave: str) -> Optional[Usuario]:
        usuario = self.usuario_dao.obtener_por_nombre_usuario(nombre_usuario)
        if usuario and usuario.clave and check_password(clave, usuario.clave):
            usuario.tipo = usuario.tipo.upper() if usuario.tipo else "PACIENTE"
            return usuario
        return None
