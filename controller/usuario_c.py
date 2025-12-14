from typing import Optional, List
from models.usuario import Usuario
from dao.usuario_dao import UsuarioDAO


class UsuarioController:
    def __init__(self, dao: UsuarioDAO):
        self.dao = dao

    def listar(self) -> List[Usuario]:
        return self.dao.listar()

    def obtener_por_id(self, usuario_id: int) -> Optional[Usuario]:
        return self.dao.obtener_por_id(usuario_id)

    def crear_usuario(self, usuario: Usuario) -> bool:
        return self.dao.crear(usuario)

    def actualizar_usuario(self, usuario: Usuario) -> bool:
        return self.dao.actualizar(usuario)

    def eliminar_usuario(self, usuario_id: int) -> bool:
        return self.dao.eliminar(usuario_id)
