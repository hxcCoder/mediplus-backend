from models.receta import Receta
from dao.receta_dao import RecetaDAO

class RecetaController:
    def __init__(self):
        self.dao = RecetaDAO()

    def listar_recetas(self) -> list[Receta]:
        return self.dao.listar_todas()

    def obtener_receta_por_id(self, id_receta: int) -> Receta | None:
        return self.dao.obtener_por_id(id_receta)

    def crear_receta(self, receta: Receta) -> bool:
        return self.dao.crear(receta)

    def actualizar_receta(self, receta: Receta) -> bool:
        return self.dao.actualizar(receta)

    def eliminar_receta(self, id_receta: int) -> bool:
        return self.dao.eliminar(id_receta)
