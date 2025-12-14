from controller.administrador_c import AdministradorController
from models.usuario import Usuario


class FakeAdminDAO:
    def __init__(self):
        self._store = {}
        self._next = 1

    def crear(self, admin: Usuario):
        admin.id = self._next
        self._store[self._next] = admin
        self._next += 1
        return True

    def obtener_por_id(self, admin_id: int):
        return self._store.get(admin_id)

    def listar(self):
        return list(self._store.values())

    def actualizar(self, admin: Usuario):
        if admin.id in self._store:
            self._store[admin.id] = admin
            return True
        return False

    def eliminar(self, admin_id: int):
        return self._store.pop(admin_id, None) is not None


def test_admin_crud():
    dao = FakeAdminDAO()
    ctrl = AdministradorController()
    ctrl.dao = dao

    a = Usuario(nombre_usuario="admin", clave="x", nombre="Admin", apellido="One", tipo="ADMIN")
    assert ctrl.crear_admin(a)
    assert len(ctrl.listar_admins()) == 1

    got = ctrl.obtener_admin(1)
    assert got and got.nombre_usuario == "admin"

    got.apellido = "Two"
    assert ctrl.actualizar_admin(got)
    assert ctrl.obtener_admin(1).apellido == "Two"

    assert ctrl.eliminar_admin(1)
    assert ctrl.obtener_admin(1) is None
