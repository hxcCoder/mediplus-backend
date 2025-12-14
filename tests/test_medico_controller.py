from controller.medico_c import MedicoController
from models.medico import Medico


class FakeMedicoDAO:
    def __init__(self):
        self._store = {}
        self._next = 1

    def crear(self, medico: Medico):
        medico.id = self._next
        self._store[self._next] = medico
        self._next += 1
        return True

    def obtener_por_id(self, medico_id: int):
        return self._store.get(medico_id)

    def listar(self):
        return list(self._store.values())

    def actualizar(self, medico: Medico):
        if medico.id in self._store:
            self._store[medico.id] = medico
            return True
        return False

    def eliminar(self, medico_id: int):
        return self._store.pop(medico_id, None) is not None


def test_medico_crud():
    dao = FakeMedicoDAO()
    ctrl = MedicoController()
    ctrl.dao = dao

    m = Medico(nombre_usuario="m1", clave="c", nombre="Ana", apellido="Perez")
    assert ctrl.crear_medico(m)
    assert len(ctrl.listar()) == 1

    got = ctrl.obtener_por_id(1)
    assert got and got.nombre_usuario == "m1"

    got.nombre = "Ana Maria"
    assert ctrl.actualizar_medico(got)
    assert ctrl.obtener_por_id(1).nombre == "Ana Maria"

    assert ctrl.eliminar(1)
    assert ctrl.obtener_por_id(1) is None
