from models.consulta import Consulta
from dao.consulta_dao import ConsultaDAO  # Asegúrate que el path coincide

class ConsultaController:
    def __init__(self):
        self.dao = ConsultaDAO()

    def crear_consulta(self, consulta: Consulta) -> bool:
        return self.dao.crear(consulta)

    def obtener_por_id(self, consulta_id: int) -> Consulta | None:
        return self.dao.obtener_por_id(consulta_id)

    def listar(self) -> list[Consulta]:
        return self.dao.listar()

    def actualizar_consulta(self, consulta: Consulta) -> bool:
        return self.dao.actualizar(consulta)

    def eliminar(self, consulta_id: int) -> bool:
        return self.dao.eliminar(consulta_id)
