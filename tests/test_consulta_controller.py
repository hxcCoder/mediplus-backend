from controller.consulta_c import ConsultaController
from models.consulta import Consulta


class FakeConsultaDAO:
    def __init__(self):
        self._store = {}
        self._next = 1

    def crear(self, consulta: Consulta):
        consulta.id = self._next
        self._store[self._next] = consulta
        self._next += 1
        return True

    def obtener_por_id(self, consulta_id: int):
        return self._store.get(consulta_id)

    def listar(self):
        return list(self._store.values())

    def actualizar(self, consulta: Consulta):
        if consulta.id in self._store:
            self._store[consulta.id] = consulta
            return True
        return False

    def eliminar(self, consulta_id: int):
        return self._store.pop(consulta_id, None) is not None


def test_consulta_crud():
    dao = FakeConsultaDAO()
    ctrl = ConsultaController()
    ctrl.dao = dao

    c = Consulta(id_paciente=1, id_medico=2, id_receta=None, fecha="2025-12-13", comentarios="OK", valor=20000)
    assert ctrl.crear_consulta(c)
    assert len(ctrl.listar()) == 1

    got = ctrl.obtener_por_id(1)
    assert got and got.comentarios == "OK"

    got.comentarios = "Updated"
    assert ctrl.actualizar_consulta(got)
    assert ctrl.obtener_por_id(1).comentarios == "Updated"

    assert ctrl.eliminar(1)
    assert ctrl.obtener_por_id(1) is None
