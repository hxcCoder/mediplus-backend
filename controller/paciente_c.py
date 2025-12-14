# controller/paciente_c.py
from dao.paciente_dao import PacienteDAO
from models.paciente import Paciente

class PacienteController:
    def __init__(self):
        self.dao = PacienteDAO()

    def crear_paciente(self, paciente: Paciente):
        return self.dao.crear(paciente)

    def obtener_paciente(self, paciente_id: int) -> Paciente | None:
        return self.dao.obtener_por_id(paciente_id)

    def listar_pacientes(self) -> list[Paciente]:
        return self.dao.listar()

    def actualizar_paciente(self, paciente: Paciente):
        return self.dao.actualizar(paciente)

    def eliminar_paciente(self, paciente_id: int):
        return self.dao.eliminar(paciente_id)
