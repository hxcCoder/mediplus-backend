# controller/consulta_c.py
from typing import Optional, List
from models.consulta import Consulta
from dao.consulta_dao import ConsultaDAO

class ConsultaController:
    def __init__(self):
        self.dao = ConsultaDAO()

    def crear_consulta(self, consulta: Consulta) -> bool:
        """Crea una nueva consulta con validaciones básicas"""
        if not consulta.id_paciente or not consulta.id_medico:
            print("Se requiere el ID de paciente y médico para crear la consulta")
            return False
        if consulta.valor is not None and consulta.valor < 0:
            print("El valor de la consulta no puede ser negativo")
            return False
        return self.dao.crear(consulta)

    def obtener_consulta_por_id(self, consulta_id: int) -> Optional[Consulta]:
        return self.dao.obtener_por_id(consulta_id)

    def listar_consultas(self) -> List[Consulta]:
        return self.dao.listar()

    def actualizar_consulta(self, consulta: Consulta) -> bool:
        if not consulta.id:
            print("Se requiere el ID de la consulta para actualizar")
            return False
        return self.dao.actualizar(consulta)

    def eliminar_consulta(self, consulta_id: int) -> bool:
        return self.dao.eliminar(consulta_id)
