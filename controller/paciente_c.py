# controller/paciente_c.py
from typing import Optional, List
from models.paciente import Paciente
from dao.paciente_dao import PacienteDAO

class PacienteController:
    def __init__(self):
        self.dao = PacienteDAO()

    def crear_paciente(self, paciente: Paciente) -> bool:
        """Crea un nuevo paciente con validaciones básicas"""
        if not paciente.nombre_usuario or not paciente.clave:
            print("El nombre de usuario y la contraseña son obligatorios")
            return False
        if not paciente.comuna:
            print("La comuna es obligatoria")
            return False
        return self.dao.crear(paciente)

    def obtener_paciente_por_id(self, paciente_id: int) -> Optional[Paciente]:
        return self.dao.obtener_por_id(paciente_id)

    def listar_pacientes(self) -> List[Paciente]:
        return self.dao.listar()

    def actualizar_paciente(self, paciente: Paciente) -> bool:
        if not paciente.id:
            print("El ID del paciente es obligatorio para actualizar")
            return False
        return self.dao.actualizar(paciente)

    def eliminar_paciente(self, paciente_id: int) -> bool:
        return self.dao.eliminar(paciente_id)
