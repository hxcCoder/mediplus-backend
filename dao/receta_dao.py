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
                VALUES (:1, :2, :3, :4, :5, :6)
            """, (
                receta.id_paciente,
                receta.id_medico,
                receta.descripcion,
                receta.medicamentos_recetados,
                receta.costo_clp,
                receta.fecha
            ))
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
                WHERE id = :1
            """, (id_receta,))
            row = cursor.fetchone()
            if row:
                return Receta(*row)
            return None
        finally:
            cursor.close()
            conn.close()

    def listar_todas(self) -> list[Receta]:
        conn = get_connection()
        cursor = conn.cursor()
        recetas = []
        try:
            cursor.execute("""
                SELECT id, id_paciente, id_medico, descripcion, medicamentos_recetados, costo_clp, fecha
                FROM receta
                ORDER BY fecha DESC
            """)
            rows = cursor.fetchall()
            for row in rows:
                recetas.append(Receta(*row))
            return recetas
        finally:
            cursor.close()
            conn.close()

    def actualizar(self, receta: Receta) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE receta
                SET id_paciente=:1, id_medico=:2, descripcion=:3,
                    medicamentos_recetados=:4, costo_clp=:5, fecha=:6
                WHERE id=:7
            """, (
                receta.id_paciente,
                receta.id_medico,
                receta.descripcion,
                receta.medicamentos_recetados,
                receta.costo_clp,
                receta.fecha,
                receta.id
            ))
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
            cursor.execute("DELETE FROM receta WHERE id = :1", (id_receta,))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print("Error al eliminar receta:", e)
            return False
        finally:
            cursor.close()
            conn.close()
