from dao.consulta_dao import ConsultaDAO
from models.consulta import Consulta
from typing import List, Optional

class ConsultaController:
    def __init__(self):
        self.dao = ConsultaDAO()

    def listar(self, id_medico: Optional[int] = None) -> List[Consulta]:
        """Lista todas las consultas o solo las de un médico específico"""
        if id_medico is not None:
            return self.dao.listar_por_medico(id_medico)
        return self.dao.listar()

    def crear(self, consulta: Consulta) -> bool:
        return self.dao.crear(consulta)

    def obtener_por_id(self, consulta_id: int) -> Optional[Consulta]:
        return self.dao.obtener_por_id(consulta_id)

    def actualizar(self, consulta: Consulta) -> bool:
        return self.dao.actualizar(consulta)

    def eliminar(self, consulta_id: int) -> bool:
        return self.dao.eliminar(consulta_id)
