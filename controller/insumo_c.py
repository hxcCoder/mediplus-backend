from models.insumo import Insumo
from dao.insumo_dao import InsumoDAO

class InsumoController:
    def __init__(self):
        self.dao = InsumoDAO()

    def listar_insumos(self) -> list[Insumo]:
        return self.dao.listar()

    def obtener_insumo_por_id(self, insumo_id: int) -> Insumo | None:
        return self.dao.obtener_por_id(insumo_id)

    def crear_insumo(self, nombre: str, tipo: str, stock: int, costo_usd: float) -> bool:
        insumo = Insumo(id=None, nombre=nombre, tipo=tipo, stock=stock, costo_usd=costo_usd)
        return self.dao.crear(insumo)

    def actualizar_insumo(self, insumo_id: int, nombre: str, tipo: str, stock: int, costo_usd: float) -> bool:
        insumo = self.dao.obtener_por_id(insumo_id)
        if not insumo:
            return False
        insumo.nombre = nombre
        insumo.tipo = tipo
        insumo.stock = stock
        insumo.costo_usd = costo_usd
        return self.dao.actualizar(insumo)

    def eliminar_insumo(self, insumo_id: int) -> bool:
        return self.dao.eliminar(insumo_id)
