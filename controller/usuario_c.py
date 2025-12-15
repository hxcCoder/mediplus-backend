from typing import Optional, List
from models.usuario import Usuario
from dao.usuario_dao import UsuarioDAO

class UsuarioController:
    def __init__(self, dao: Optional[UsuarioDAO] = None):
        self.dao = dao or UsuarioDAO()

    def crear_usuario(self, usuario: Usuario) -> bool:
        return self.dao.crear(usuario)

    def obtener_usuario_por_id(self, usuario_id: int) -> Optional[Usuario]:
        return self.dao.obtener_por_id(usuario_id)

    def obtener_usuario_por_nombre(self, nombre_usuario: str) -> Optional[Usuario]:
        return self.dao.obtener_por_nombre_usuario(nombre_usuario)

    def login_usuario(self, nombre_usuario: str, clave: str) -> Optional[Usuario]:
        return self.dao.login(nombre_usuario, clave)

    def listar_usuarios(self) -> List[Usuario]:
        return self.dao.listar()

    def actualizar_usuario(self, usuario: Usuario) -> bool:
        return self.dao.actualizar(usuario)

    def eliminar_usuario(self, usuario_id: int) -> bool:
        return self.dao.eliminar(usuario_id)
