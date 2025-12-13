from dao.receta_dao import RecetaDAO
from models.receta import Receta

class RecetaController:
    def __init__(self):
        self.dao = RecetaDAO()

    # Crear receta
    def crear(self, receta: Receta) -> bool:
        return self.dao.crear(receta)

    # Obtener receta por ID
    def obtener_por_id(self, id_receta: int) -> Receta | None:
        return self.dao.obtener_por_id(id_receta)

    # Listar todas las recetas
    def listar_todas(self) -> list[Receta]:
        return self.dao.listar_todas()

    # Actualizar receta
    def actualizar(self, receta: Receta) -> bool:
        return self.dao.actualizar(receta)

    # Eliminar receta
    def eliminar(self, id_receta: int) -> bool:
        return self.dao.eliminar(id_receta)
