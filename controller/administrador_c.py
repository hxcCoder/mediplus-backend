# controller/administrador_c.py
from typing import Optional, List
from models.usuario import Usuario
from dao.administrador_dao import AdministradorDAO

class AdministradorController:
    def __init__(self):
        self.dao = AdministradorDAO()

    def crear_admin(self, admin: Usuario) -> bool:
        if not admin.nombre_usuario or not admin.clave:
            print("Se requiere nombre de usuario y clave para crear administrador")
            return False
        return self.dao.crear(admin)

    def obtener_admin_por_id(self, admin_id: int) -> Optional[Usuario]:
        return self.dao.obtener_por_id(admin_id)

    def listar_admins(self) -> List[Usuario]:
        return self.dao.listar()

    def actualizar_admin(self, admin: Usuario) -> bool:
        if not admin.id:
            print("Se requiere ID del administrador para actualizar")
            return False
        return self.dao.actualizar(admin)

    def eliminar_admin(self, admin_id: int) -> bool:
        return self.dao.eliminar(admin_id)
