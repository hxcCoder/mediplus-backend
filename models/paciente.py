from models.usuario import Usuario

class Paciente(Usuario):
    def __init__(self, comuna=None, fecha_primera_visita=None, **kwargs):
        super().__init__(**kwargs)
        self.comuna = comuna
        self.fecha_primera_visita = fecha_primera_visita
