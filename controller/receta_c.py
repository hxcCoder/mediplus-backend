# controller/receta_c.py
from typing import Optional
from dao.receta_dao import RecetaDAO
from models.receta import Receta


class RecetaController:
    def __init__(self, dao: Optional[RecetaDAO] = None):
        self.dao = dao or RecetaDAO()

    def listar(self):
        """Retorna todas las recetas"""
        return self.dao.listar_todas()

    def crear_receta(self, data: dict):
        """Crea una receta a partir de un diccionario de datos"""
        try:
            receta = Receta(
                id_paciente=data.get("id_paciente"),
                id_medico=data.get("id_medico"),
                descripcion=data.get("descripcion"),
                medicamentos_recetados=data.get("medicamentos_recetados"),
                costo_clp=data.get("costo_clp"),
                fecha=data.get("fecha")
            )
            return self.dao.crear(receta)
        except Exception as e:
            print("Error creando receta:", e)
            return False

    def obtener_por_id(self, id_receta: int):
        return self.dao.obtener_por_id(id_receta)

    def actualizar_receta(self, receta):
        try:
            return self.dao.actualizar(receta)
        except Exception as e:
            print("Error actualizando receta:", e)
            return False

    def eliminar(self, id_receta):
        """Elimina una receta por ID"""
        try:
            return self.dao.eliminar(id_receta)
        except Exception as e:
            print("Error eliminando receta:", e)
            return False
