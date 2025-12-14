# controller/consulta_c.py
from dao.consulta_dao import ConsultaDAO
from models.consulta import Consulta

class ConsultaController:
    def __init__(self):
        self.dao = ConsultaDAO()

    # Crear consulta
    def crear_consulta(self, consulta: Consulta) -> bool:
        if not consulta.id_paciente or not consulta.id_medico:
            raise ValueError("La consulta debe tener paciente y médico asignados")
        return self.dao.crear(consulta)

    # Obtener consulta por ID
    def obtener_por_id(self, consulta_id: int) -> Consulta | None:
        return self.dao.obtener_por_id(consulta_id)

    # Listar todas las consultas
    def listar(self) -> list[Consulta]:
        return self.dao.listar()

    # Actualizar consulta
    def actualizar_consulta(self, consulta: Consulta) -> bool:
        if not consulta.id:
            raise ValueError("No se puede actualizar una consulta sin ID")
        return self.dao.actualizar(consulta)

    # Eliminar consulta
    def eliminar(self, consulta_id: int) -> bool:
        if not consulta_id:
            raise ValueError("Se requiere el ID de la consulta para eliminarla")
        return self.dao.eliminar(consulta_id)
