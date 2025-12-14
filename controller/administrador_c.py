# controller/administrador_c.py
from dao.administrador_dao import AdministradorDAO
from models.usuario import Usuario

class AdministradorController:

    def __init__(self):
        self.dao = AdministradorDAO()

    def crear_admin(self, admin: Usuario) -> bool:
        return self.dao.crear(admin)

    def obtener_admin(self, admin_id: int) -> Usuario | None:
        return self.dao.obtener_por_id(admin_id)

    def listar_admins(self) -> list[Usuario]:
        return self.dao.listar()

    def actualizar_admin(self, admin: Usuario) -> bool:
        return self.dao.actualizar(admin)

    def eliminar_admin(self, admin_id: int) -> bool:
        return self.dao.eliminar(admin_id)
