from typing import Optional

class Consulta:
    def __init__(
        self,
        id: Optional[int],
        id_paciente: int,
        id_medico: int,
        id_receta: Optional[int],
        fecha: str,
        comentarios: str,
        valor: float
    ):
        self.id = id
        self.id_paciente = id_paciente
        self.id_medico = id_medico
        self.id_receta = id_receta
        self.fecha = fecha
        self.comentarios = comentarios
        self.valor = valor
