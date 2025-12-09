# models/administrador.py
from models.usuario import Usuario

class Administrador(Usuario):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_dict(self):
        # Se puede extender más adelante con campos propios de admin
        return super().to_dict()
