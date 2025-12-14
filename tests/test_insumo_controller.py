from controller.insumo_c import InsumoController
from models.insumo import Insumo


class FakeDAO:
    def __init__(self):
        self.insumos = {}
        self._id = 1

    def crear(self, insumo: Insumo):
        insumo.id = self._id
        self.insumos[self._id] = insumo
        self._id += 1
        return True

    def listar(self):
        return list(self.insumos.values())

    def obtener_por_id(self, insumo_id: int):
        return self.insumos.get(insumo_id)

    def actualizar(self, insumo: Insumo):
        if insumo.id not in self.insumos:
            return False
        self.insumos[insumo.id] = insumo
        return True

    def eliminar(self, insumo_id: int):
        if insumo_id in self.insumos:
            del self.insumos[insumo_id]
            return True
        return False


def test_insumo_crud():
    ctrl = InsumoController()
    ctrl.dao = FakeDAO()

    assert ctrl.crear({"nombre": "Algodón", "tipo": "consumible", "stock": 10, "costo_usd": 1.5})
    lista = ctrl.listar()
    assert len(lista) == 1
    ins = lista[0]
    assert ins.nombre == "Algodón"

    ok = ctrl.actualizar(ins.id, {"stock": 20})
    assert ok
    updated = ctrl.dao.obtener_por_id(ins.id)
    assert updated.stock == 20

    assert ctrl.eliminar(ins.id)
    assert len(ctrl.listar()) == 0
