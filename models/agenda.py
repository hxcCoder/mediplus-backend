# models/agenda.py
class Agenda:
    def __init__(self, id=None, id_paciente=None, id_medico=None, fecha_consulta=None, estado=None):
        self.id = id
        self.id_paciente = id_paciente
        self.id_medico = id_medico
        self.fecha_consulta = fecha_consulta  
        self.estado = estado  

    def to_dict(self):
        return {
            "id": self.id,
            "id_paciente": self.id_paciente,
            "id_medico": self.id_medico,
            "fecha_consulta": self.fecha_consulta,
            "estado": self.estado
        }
