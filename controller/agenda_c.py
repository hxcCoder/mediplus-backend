# controller/agenda_c.py
from typing import Optional, List
from models.agenda import Agenda
from dao.agenda_dao import AgendaDAO

class AgendaController:
    def __init__(self):
        self.dao = AgendaDAO()

    def crear_agenda(self, agenda: Agenda) -> bool:
        if not agenda.id_paciente or not agenda.id_medico:
            print("Se requiere ID de paciente y médico para crear la agenda")
            return False
        return self.dao.crear(agenda)

    def obtener_agenda_por_id(self, agenda_id: int) -> Optional[Agenda]:
        return self.dao.obtener_por_id(agenda_id)

    def listar_agendas(self) -> List[Agenda]:
        return self.dao.listar()

    def actualizar_agenda(self, agenda: Agenda) -> bool:
        if not agenda.id:
            print("Se requiere el ID de la agenda para actualizar")
            return False
        return self.dao.actualizar(agenda)

    def eliminar_agenda(self, agenda_id: int) -> bool:
        return self.dao.eliminar(agenda_id)
