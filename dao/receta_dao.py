from db.connection import get_connection
from models.receta import Receta

class RecetaDAO:

    def crear(self, receta: Receta) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO receta
                (id_paciente, id_medico, descripcion, medicamentos_recetados, costo_clp, fecha)
                VALUES (:id_paciente, :id_medico, :descripcion, :medicamentos, :costo, :fecha)
            """, {
                "id_paciente": receta.id_paciente,
                "id_medico": receta.id_medico,
                "descripcion": receta.descripcion,
                "medicamentos": receta.medicamentos_recetados,
                "costo": receta.costo_clp,
                "fecha": receta.fecha
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

    def obtener_por_id(self, id_receta: int) -> Receta | None:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT id, id_paciente, id_medico, descripcion, medicamentos_recetados, costo_clp, fecha
                FROM receta
                WHERE id = :id
            """, {"id": id_receta})
            row = cursor.fetchone()
            return Receta(*row) if row else None
        finally:
            cursor.close()
            conn.close()

    def listar_todas(self) -> list[Receta]:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT id, id_paciente, id_medico, descripcion, medicamentos_recetados, costo_clp, fecha
                FROM receta
                ORDER BY fecha DESC
            """)
            rows = cursor.fetchall()
            return [Receta(*r) for r in rows]
        finally:
            cursor.close()
            conn.close()

    def actualizar(self, receta: Receta) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE receta
                SET id_paciente=:id_paciente, id_medico=:id_medico, descripcion=:descripcion,
                    medicamentos_recetados=:medicamentos, costo_clp=:costo, fecha=:fecha
                WHERE id=:id
            """, {
                "id_paciente": receta.id_paciente,
                "id_medico": receta.id_medico,
                "descripcion": receta.descripcion,
                "medicamentos": receta.medicamentos_recetados,
                "costo": receta.costo_clp,
                "fecha": receta.fecha,
                "id": receta.id
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
