from dao.medico_dao import MedicoDAO
from models.medico import Medico

class MedicoController:

    def __init__(self):
        self.dao = MedicoDAO()

    def crear_medico(self, medico: Medico) -> bool:
        if not medico.clave:
            raise ValueError("La clave no puede ser None")
        return self.dao.crear(medico)

    def obtener_por_id(self, medico_id: int) -> Medico | None:
        return self.dao.obtener_por_id(medico_id)

    def listar(self) -> list[Medico]:
        return self.dao.listar()

    def actualizar_medico(self, medico: Medico) -> bool:
        return self.dao.actualizar(medico)

    def eliminar(self, medico_id: int) -> bool:
        return self.dao.eliminar(medico_id)
