# controller/receta_c.py
from typing import Optional, List
from models.receta import Receta
from dao.receta_dao import RecetaDAO

class RecetaController:
    def __init__(self):
        self.dao = RecetaDAO()

    def crear_receta(self, receta: Receta) -> bool:
        """Crea una nueva receta con validaciones básicas"""
        if not receta.id_paciente or not receta.id_medico:
            print("Se requiere el ID de paciente y médico para crear una receta")
            return False
        if receta.costo_clp is not None and receta.costo_clp < 0:
            print("El costo de la receta no puede ser negativo")
            return False
        return self.dao.crear(receta)

    def obtener_receta_por_id(self, id_receta: int) -> Optional[Receta]:
        return self.dao.obtener_por_id(id_receta)

    def listar_recetas(self) -> List[Receta]:
        return self.dao.listar_todas()

    def actualizar_receta(self, receta: Receta) -> bool:
        if not receta.id:
            print("Se requiere el ID de la receta para actualizar")
            return False
        return self.dao.actualizar(receta)

    def eliminar_receta(self, id_receta: int) -> bool:
        return self.dao.eliminar(id_receta)
