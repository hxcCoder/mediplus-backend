from typing import List, Optional
from dao.receta_dao import RecetaDAO
from models.receta import Receta

class RecetaController:
    def __init__(self):
        self.dao = RecetaDAO()

    def crear_receta(self, receta: Receta) -> bool:
        """Crea una nueva receta en la base de datos."""
        return self.dao.crear(receta)

    def obtener_receta_por_id(self, id_receta: int) -> Optional[Receta]:
        """Obtiene una receta por su ID. Retorna None si no existe."""
        return self.dao.obtener_por_id(id_receta)

    def listar_recetas(self) -> List[Receta]:
        """Devuelve todas las recetas como lista."""
        return self.dao.listar_todas()

    def actualizar_receta(self, receta: Receta) -> bool:
        """Actualiza los datos de una receta existente."""
        return self.dao.actualizar(receta)

    def eliminar_receta(self, id_receta: int) -> bool:
        """Elimina una receta por su ID."""
        return self.dao.eliminar(id_receta)
