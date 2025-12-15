from db.connection import get_connection
from models.consulta import Consulta

class ConsultaDAO:

    def crear(self, consulta: Consulta) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            if not consulta.id_paciente or not consulta.id_medico:
                raise ValueError("Se requiere ID de paciente y médico")
            cursor.execute("""
                INSERT INTO consulta (id_paciente, id_medico, id_receta, fecha, comentarios, valor)
                VALUES (:id_paciente, :id_medico, :id_receta, :fecha, :comentarios, :valor)
            """, {
                "id_paciente": consulta.id_paciente,
                "id_medico": consulta.id_medico,
                "id_receta": consulta.id_receta,
                "fecha": consulta.fecha,
                "comentarios": consulta.comentarios,
                "valor": consulta.valor
            })
            conn.commit()
            return True
        finally:
            cursor.close()
            conn.close()

    def obtener_por_id(self, consulta_id: int) -> Consulta | None:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, id_paciente, id_medico, id_receta, fecha, comentarios, valor FROM consulta WHERE id = :id", {"id": consulta_id})
            row = cursor.fetchone()
            return Consulta(*row) if row else None
        finally:
            cursor.close()
            conn.close()

    def listar(self) -> list[Consulta]:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, id_paciente, id_medico, id_receta, fecha, comentarios, valor FROM consulta ORDER BY fecha DESC")
            rows = cursor.fetchall()
            return [Consulta(*r) for r in rows]
        finally:
            cursor.close()
            conn.close()

    def actualizar(self, consulta: Consulta) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE consulta
                SET id_paciente=:id_paciente, id_medico=:id_medico, id_receta=:id_receta,
                    fecha=:fecha, comentarios=:comentarios, valor=:valor
                WHERE id=:id
            """, {
                "id_paciente": consulta.id_paciente,
                "id_medico": consulta.id_medico,
                "id_receta": consulta.id_receta,
                "fecha": consulta.fecha,
                "comentarios": consulta.comentarios,
                "valor": consulta.valor,
                "id": consulta.id
            })
            conn.commit()
            return True
        finally:
            cursor.close()
            conn.close()

    def eliminar(self, consulta_id: int) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM consulta WHERE id=:id", {"id": consulta_id})
            conn.commit()
            return True
        finally:
            cursor.close()
            conn.close()
