class UsuarioController:

    def __init__(self, usuario_dao):
        self.usuario_dao = usuario_dao

    def listar(self):
        return self.usuario_dao.listar()

    def obtener_por_id(self, id_usuario):
        return self.usuario_dao.obtener_por_id(id_usuario)
