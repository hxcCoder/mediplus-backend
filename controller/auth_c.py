from models.usuario import Usuario
from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from dao.usuario_dao import UsuarioDAO
from utils.security import hash_password


class AuthController:
    """Controller para registro/login. Acepta un DAO opcional para facilitar pruebas."""

    def __init__(self, usuario_dao: Optional['UsuarioDAO'] = None):
        # Importar DAO solo cuando sea necesario para evitar dependencias pesadas en tiempo de import
        if usuario_dao is None:
            from dao.usuario_dao import UsuarioDAO
            usuario_dao = UsuarioDAO()
        self.usuario_dao = usuario_dao

    def registrar_usuario(self, usuario: Usuario) -> bool:
        # Validación básica
        if not usuario.nombre_usuario or not usuario.clave:
            return False

        # Evitar usuarios duplicados
        existente = self.usuario_dao.obtener_por_nombre_usuario(usuario.nombre_usuario)
        if existente:
            return False

        # Hash de contraseña y almacenar como str
        usuario.clave = hash_password(usuario.clave).decode("utf-8")

        return self.usuario_dao.crear(usuario)

    def login(self, nombre_usuario: str, clave: str) -> Usuario | None:
        """Intenta autenticar y devuelve Usuario o None"""
        if not nombre_usuario or not clave:
            return None
        return self.usuario_dao.login(nombre_usuario, clave)
