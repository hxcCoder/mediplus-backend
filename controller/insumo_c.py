from typing import List, Dict, Optional
from models.insumo import Insumo


class InsumoController:
    def __init__(self, dao: Optional[object] = None):
        # Permitir inyección de DAO para tests
        if dao is None:
            from dao.insumo_dao import InsumoDAO
            dao = InsumoDAO()
        self.dao = dao

    def listar(self) -> List[Insumo]:
        return self.dao.listar()  # devuelve lista de objetos Insumo

    def crear(self, datos: Dict) -> bool:
        try:
            insumo = Insumo(**datos)  # mapear datos recibidos al modelo
            return self.dao.crear(insumo)
        except Exception as e:
            print("Error en InsumoController.crear:", e)
            return False

    def actualizar(self, insumo_id: int, datos: Dict) -> bool:
        try:
            insumo = self.dao.obtener_por_id(insumo_id)
            if not insumo:
                return False
            for key, value in datos.items():
                if hasattr(insumo, key):
                    setattr(insumo, key, value)
            return self.dao.actualizar(insumo)
        except Exception as e:
            print("Error en InsumoController.actualizar:", e)
            return False

    def eliminar(self, insumo_id: int) -> bool:
        try:
            return self.dao.eliminar(insumo_id)
        except Exception as e:
            print("Error en InsumoController.eliminar:", e)
            return False
