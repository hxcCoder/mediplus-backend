class Usuario:
    def __init__(self, id=None, nombre_usuario=None, clave=None, nombre=None, apellido=None,
                fecha_nacimiento=None, telefono=None, email=None, tipo=None):
        self.id = id
        self.nombre_usuario = nombre_usuario
        self.clave = clave
        self.nombre = nombre
        self.apellido = apellido
        self.fecha_nacimiento = fecha_nacimiento
        self.telefono = telefono
        self.email = email
        self.tipo = tipo  # paciente / medico / admin

    def to_dict(self):
        return {
            "id": self.id,
            "nombre_usuario": self.nombre_usuario,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "fecha_nacimiento": self.fecha_nacimiento,
            "telefono": self.telefono,
            "email": self.email,
            "tipo": self.tipo
        }
