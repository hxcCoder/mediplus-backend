class Receta:
    def __init__(self, id=None, id_paciente=None, id_medico=None, descripcion=None,
                medicamentos_recetados=None, costo_clp=None, fecha=None):
        self.id = id
        self.id_paciente = id_paciente
        self.id_medico = id_medico
        self.descripcion = descripcion
        self.medicamentos_recetados = medicamentos_recetados
        self.costo_clp = costo_clp
        self.fecha = fecha
