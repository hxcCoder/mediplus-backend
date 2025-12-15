# controller/insumo_c.py
from typing import Optional, List
from models.insumo import Insumo
from dao.insumo_dao import InsumoDAO

class InsumoController:
    def __init__(self):
        self.dao = InsumoDAO()

    def crear_insumo(self, insumo: Insumo) -> bool:
        """Crea un nuevo insumo con validaciones básicas"""
        if not insumo.nombre:
            print("El nombre del insumo es obligatorio")
            return False
        if insumo.stock is None or insumo.stock < 0:
            print("El stock debe ser un número mayor o igual a 0")
            return False
        if insumo.costo_usd is None or insumo.costo_usd < 0:
            print("El costo en USD debe ser un número mayor o igual a 0")
            return False
        return self.dao.crear(insumo)

    def obtener_insumo_por_id(self, insumo_id: int) -> Optional[Insumo]:
        return self.dao.obtener_por_id(insumo_id)

    def listar_insumos(self) -> List[Insumo]:
        return self.dao.listar()

    def actualizar_insumo(self, insumo: Insumo) -> bool:
        if not insumo.id:
            print("El ID del insumo es obligatorio para actualizar")
            return False
        return self.dao.actualizar(insumo)

    def eliminar_insumo(self, insumo_id: int) -> bool:
        return self.dao.eliminar(insumo_id)
