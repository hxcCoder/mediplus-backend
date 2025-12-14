from controller.paciente_c import PacienteController
from models.paciente import Paciente


class FakePacienteDAO:
    def __init__(self):
        self._store = {}
        self._next = 1

    def crear(self, paciente: Paciente):
        paciente.id = self._next
        self._store[self._next] = paciente
        self._next += 1
        return True

    def obtener_por_id(self, paciente_id: int):
        return self._store.get(paciente_id)

    def listar(self):
        return list(self._store.values())

    def actualizar(self, paciente: Paciente):
        if paciente.id in self._store:
            self._store[paciente.id] = paciente
            return True
        return False

    def eliminar(self, paciente_id: int):
        return self._store.pop(paciente_id, None) is not None


def test_paciente_crud():
    dao = FakePacienteDAO()
    ctrl = PacienteController()
    ctrl.dao = dao

    p = Paciente(nombre_usuario="p1", clave="c", nombre="A", apellido="B")
    assert ctrl.crear_paciente(p)
    assert len(ctrl.listar_pacientes()) == 1

    got = ctrl.obtener_paciente(1)
    assert got and got.nombre_usuario == "p1"

    got.nombre = "C"
    assert ctrl.actualizar_paciente(got)
    assert ctrl.obtener_paciente(1).nombre == "C"

    assert ctrl.eliminar_paciente(1)
    assert ctrl.obtener_paciente(1) is None
