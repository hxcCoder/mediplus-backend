# dao/receta_dao.py
from typing import List, Optional
from db.connection import get_connection
from models.receta import Receta
from datetime import datetime

class RecetaDAO:

    def _parse_fecha(self, fecha):
        """Convierte un string a datetime si es necesario."""
        if isinstance(fecha, str):
            try:
                return datetime.strptime(fecha, "%Y-%m-%d")  # Ajusta al formato que uses
            except ValueError:
                print("Formato de fecha inválido, usando fecha actual")
                return datetime.now()
        return fecha

    def crear(self, receta: Receta) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            fecha = self._parse_fecha(receta.fecha)
            cursor.execute("""
                INSERT INTO receta
                (id, id_paciente, id_medico, descripcion, medicamentos_recetados, costo_clp, fecha)
                VALUES (receta_seq.NEXTVAL, :id_paciente, :id_medico, :descripcion, :medicamentos, :costo, :fecha)
            """, {
                "id_paciente": receta.id_paciente,
                "id_medico": receta.id_medico,
                "descripcion": receta.descripcion,
                "medicamentos": receta.medicamentos_recetados,
                "costo": receta.costo_clp,
                "fecha": fecha
            })
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print("Error al crear receta:", e)
            return False
        finally:
            cursor.close()
            conn.close()

    def obtener_por_id(self, id_receta: int) -> Optional[Receta]:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT id, id_paciente, id_medico, descripcion, medicamentos_recetados, costo_clp, fecha
                FROM receta
                WHERE id = :id
            """, {"id": id_receta})
            row = cursor.fetchone()
            if row:
                return Receta(*row)
            return None
        except Exception as e:
            print("Error al obtener receta:", e)
            return None
        finally:
            cursor.close()
            conn.close()

    def listar_todas(self) -> List[Receta]:
        conn = get_connection()
        cursor = conn.cursor()
        recetas = []
        try:
            cursor.execute("""
                SELECT id, id_paciente, id_medico, descripcion, medicamentos_recetados, costo_clp, fecha
                FROM receta
            """)
            rows = cursor.fetchall()
            recetas = [Receta(*row) for row in rows]
            return recetas
        except Exception as e:
            print("Error al listar recetas:", e)
            return []
        finally:
            cursor.close()
            conn.close()

    def actualizar(self, receta: Receta) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            fecha = self._parse_fecha(receta.fecha)
            cursor.execute("""
                UPDATE receta
                SET id_paciente = :id_paciente,
                    id_medico = :id_medico,
                    descripcion = :descripcion,
                    medicamentos_recetados = :medicamentos,
                    costo_clp = :costo,
                    fecha = :fecha
                WHERE id = :id
            """, {
                "id": receta.id,
                "id_paciente": receta.id_paciente,
                "id_medico": receta.id_medico,
                "descripcion": receta.descripcion,
                "medicamentos": receta.medicamentos_recetados,
                "costo": receta.costo_clp,
                "fecha": fecha
            })
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print("Error al actualizar receta:", e)
            return False
        finally:
            cursor.close()
            conn.close()

    def eliminar(self, id_receta: int) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM receta WHERE id = :id", {"id": id_receta})
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print("Error al eliminar receta:", e)
            return False
        finally:
            cursor.close()
            conn.close()
