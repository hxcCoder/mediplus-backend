# controller/auth_c.py
from typing import Optional
from models.usuario import Usuario
from dao.usuario_dao import UsuarioDAO
from utils.security import hash_password, check_password

class AuthController:
    """Controller para registro y login de usuarios."""

    def __init__(self, usuario_dao: Optional[UsuarioDAO] = None):
        self.usuario_dao = usuario_dao or UsuarioDAO()

    def registrar_usuario(self, usuario: Usuario) -> bool:
        """Registra un nuevo usuario, hasheando la contraseña."""
        if not usuario.nombre_usuario or not usuario.clave:
            return False

        # Evitar usuarios duplicados
        existente = self.usuario_dao.obtener_por_nombre_usuario(usuario.nombre_usuario)
        if existente:
            return False

        # Hashear la contraseña
        usuario.clave = hash_password(usuario.clave).decode("utf-8")
        return self.usuario_dao.crear(usuario)

    def login(self, nombre_usuario: str, clave: str) -> Optional[Usuario]:
        """Intenta autenticar y devuelve Usuario o None"""
        if not nombre_usuario or not clave:
            return None

        usuario = self.usuario_dao.obtener_por_nombre_usuario(nombre_usuario)
        if not usuario:
            return None

        if check_password(clave, usuario.clave):
            return usuario

        return None
