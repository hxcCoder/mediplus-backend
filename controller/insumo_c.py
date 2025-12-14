from typing import List, Dict
from models.insumo import Insumo
from dao.insumo_dao import InsumoDAO


class InsumoController:
    def __init__(self, dao: InsumoDAO | None = None):
        # Inyección de dependencias (buena práctica)
        self.dao: InsumoDAO = dao if dao else InsumoDAO()

    def listar(self) -> List[Insumo]:
        return self.dao.listar()

    def crear(self, datos: Dict) -> bool:
        try:
            insumo = Insumo(**datos)
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
