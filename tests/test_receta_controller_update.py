from controller.receta_c import RecetaController
from models.receta import Receta


class FakeRecetaDAO:
    def __init__(self):
        self._store = {}
        self._next = 1

    def crear(self, receta: Receta):
        receta.id = self._next
        self._store[self._next] = receta
        self._next += 1
        return True

    def obtener_por_id(self, id_receta: int):
        return self._store.get(id_receta)

    def listar_todas(self):
        return list(self._store.values())

    def actualizar(self, receta: Receta):
        if receta.id in self._store:
            self._store[receta.id] = receta
            return True
        return False

    def eliminar(self, id_receta: int):
        return self._store.pop(id_receta, None) is not None


def test_receta_crud_and_update():
    dao = FakeRecetaDAO()
    ctrl = RecetaController(dao)

    data = {"id_paciente": 1, "id_medico": 2, "descripcion": "Desc", "medicamentos_recetados": "Aspirina", "costo_clp": 5000, "fecha": "2025-12-13"}
    assert ctrl.crear_receta(data)
    recetas = ctrl.listar()
    assert len(recetas) == 1

    r = ctrl.obtener_por_id(1)
    assert r and r.descripcion == "Desc"

    r.descripcion = "Nueva"
    assert ctrl.actualizar_receta(r)
    assert ctrl.obtener_por_id(1).descripcion == "Nueva"

    assert ctrl.eliminar(1)
    assert ctrl.obtener_por_id(1) is None
