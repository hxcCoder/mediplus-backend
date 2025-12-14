from controller.receta_c import RecetaController
from models.receta import Receta


class FakeDAO:
    def __init__(self):
        self.recetas = {}
        self._id = 1

    def crear(self, receta: Receta):
        receta.id = self._id
        self.recetas[self._id] = receta
        self._id += 1
        return True

    def listar_todas(self):
        return list(self.recetas.values())

    def obtener_por_id(self, id_receta: int):
        return self.recetas.get(id_receta)

    def eliminar(self, id_receta: int):
        if id_receta in self.recetas:
            del self.recetas[id_receta]
            return True
        return False


def test_receta_crud():
    ctrl = RecetaController()
    ctrl.dao = FakeDAO()

    data = {"id_paciente": 1, "id_medico": 2, "descripcion": "Desc", "medicamentos_recetados": "Aspirina", "costo_clp": 5000, "fecha": "2025-12-13"}
    assert ctrl.crear_receta(data)
    lista = ctrl.listar()
    assert len(lista) == 1
    r = lista[0]
    assert r.id_paciente == 1

    assert ctrl.eliminar(r.id)
    assert len(ctrl.listar()) == 0
