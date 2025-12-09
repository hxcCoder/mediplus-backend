class Insumo:
    def __init__(self, id=None, nombre=None, tipo=None, stock=None, costo_usd=None):
        self.id = id
        self.nombre = nombre
        self.tipo = tipo
        self.stock = stock
        self.costo_usd = costo_usd

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "tipo": self.tipo,
            "stock": self.stock,
            "costo_usd": self.costo_usd
        }
