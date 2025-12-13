from dao.insumo_dao import InsumoDAO
from models.insumo import Insumo

class InsumoController:

    def __init__(self):
        self.dao = InsumoDAO()

    def crear(self, insumo: Insumo) -> bool:
        return self.dao.crear(insumo)

    def obtener_por_id(self, insumo_id: int) -> Insumo | None:
        return self.dao.obtener_por_id(insumo_id)

    def listar(self) -> list[Insumo]:
        return self.dao.listar()

    def actualizar(self, insumo: Insumo) -> bool:
        return self.dao.actualizar(insumo)

    def eliminar(self, insumo_id: int) -> bool:
        return self.dao.eliminar(insumo_id)
