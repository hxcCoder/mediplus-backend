from controller.usuario_c import UsuarioController
from models.usuario import Usuario


class FakeUsuarioDAO:
    def __init__(self):
        self._store = {}
        self._next = 1

    def crear(self, u: Usuario):
        u.id = self._next
        self._store[self._next] = u
        self._next += 1
        return True

    def obtener_por_id(self, id_u: int):
        return self._store.get(id_u)

    def listar(self):
        return list(self._store.values())

    def actualizar(self, u: Usuario):
        if u.id in self._store:
            self._store[u.id] = u
            return True
        return False

    def eliminar(self, id_u: int):
        return self._store.pop(id_u, None) is not None


def test_usuario_crud():
    dao = FakeUsuarioDAO()
    ctrl = UsuarioController(dao)

    u = Usuario(nombre_usuario="u1", clave="p", nombre="X", apellido="Y")
    assert ctrl.crear_usuario(u)
    assert len(ctrl.listar()) == 1

    got = ctrl.obtener_usuario(1)
    assert got and got.nombre_usuario == "u1"

    got.apellido = "Z"
    assert ctrl.actualizar_usuario(got)
    assert ctrl.obtener_usuario(1).apellido == "Z"

    assert ctrl.eliminar(1)
    assert ctrl.obtener_usuario(1) is None
