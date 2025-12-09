from models.usuario import Usuario

class Medico(Usuario):
    def __init__(self, especialidad=None, horario_atencion=None, fecha_ingreso=None, **kwargs):
        super().__init__(**kwargs)
        self.especialidad = especialidad
        self.horario_atencion = horario_atencion
        self.fecha_ingreso = fecha_ingreso
