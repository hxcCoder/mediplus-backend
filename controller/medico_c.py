# controller/medico_c.py
from typing import Optional, List
from models.medico import Medico
from dao.medico_dao import MedicoDAO

class MedicoController:
    def __init__(self):
        self.dao = MedicoDAO()

    def crear_medico(self, medico: Medico) -> bool:
        """Crea un nuevo médico con validaciones básicas"""
        if not medico.nombre_usuario or not medico.clave:
            print("El nombre de usuario y la contraseña son obligatorios")
            return False
        if not medico.especialidad:
            print("La especialidad es obligatoria")
            return False
        return self.dao.crear(medico)

    def obtener_medico_por_id(self, medico_id: int) -> Optional[Medico]:
        return self.dao.obtener_por_id(medico_id)

    def listar_medicos(self) -> List[Medico]:
        return self.dao.listar()

    def actualizar_medico(self, medico: Medico) -> bool:
        if not medico.id:
            print("El ID del médico es obligatorio para actualizar")
            return False
        return self.dao.actualizar(medico)

    def eliminar_medico(self, medico_id: int) -> bool:
        return self.dao.eliminar(medico_id)
