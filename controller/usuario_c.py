from models.usuario import Usuario

class UsuarioController:

    def __init__(self, usuario_dao):
        self.usuario_dao = usuario_dao

    def listar(self) -> list[Usuario]:
        return self.usuario_dao.listar()

    def obtener_por_id(self, id_usuario: int) -> Usuario | None:
        return self.usuario_dao.obtener_por_id(id_usuario)

    def obtener_usuario(self, id_usuario: int) -> Usuario | None:
        return self.obtener_por_id(id_usuario)

    def crear(self, usuario: Usuario) -> bool:
        return self.usuario_dao.crear(usuario)

    def crear_usuario(self, usuario: Usuario) -> bool:
        return self.crear(usuario)

    def actualizar(self, usuario: Usuario) -> bool:
        return self.usuario_dao.actualizar(usuario)

    def actualizar_usuario(self, usuario: Usuario) -> bool:
        return self.actualizar(usuario)

    def eliminar(self, usuario_id: int) -> bool:
        return self.usuario_dao.eliminar(usuario_id)
