from typing import Optional
from datetime import date

class Usuario:
    def __init__(
        self,
        id: Optional[int] = None,
        nombre_usuario: str = "",
        clave: str = "",
        nombre: str = "",
        apellido: str = "",
        fecha_nacimiento: Optional[date] = None,
        telefono: str = "",
        email: str = "",
        tipo: str = "PACIENTE"
    ):
        self.id = id
        self.nombre_usuario = nombre_usuario
        self.clave = clave
        self.nombre = nombre
        self.apellido = apellido
        self.fecha_nacimiento = fecha_nacimiento
        self.telefono = telefono
        self.email = email
        self.tipo = tipo

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nombre_usuario": self.nombre_usuario,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "fecha_nacimiento": (
                self.fecha_nacimiento.isoformat()
                if self.fecha_nacimiento else None
            ),
            "telefono": self.telefono,
            "email": self.email,
            "tipo": self.tipo
        }
