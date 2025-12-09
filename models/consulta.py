class Consulta:
    def __init__(self, id=None, id_paciente=None, id_medico=None, id_receta=None,
                fecha=None, comentarios=None, valor=None):
        self.id = id
        self.id_paciente = id_paciente
        self.id_medico = id_medico
        self.id_receta = id_receta
        self.fecha = fecha
        self.comentarios = comentarios
        self.valor = valor
