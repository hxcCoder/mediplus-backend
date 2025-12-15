# dao/agenda_dao.py
from db.connection import get_connection
from models.agenda import Agenda

class AgendaDAO:

    def crear(self, agenda: Agenda) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            if not agenda.id_paciente or not agenda.id_medico:
                raise ValueError("Se requiere ID de paciente y médico para crear la agenda")
            cursor.execute("""
                INSERT INTO agenda (id_paciente, id_medico, fecha_consulta, estado)
                VALUES (:id_paciente, :id_medico, :fecha_consulta, :estado)
            """, {
                "id_paciente": agenda.id_paciente,
                "id_medico": agenda.id_medico,
                "fecha_consulta": agenda.fecha_consulta,
                "estado": agenda.estado
            })
            conn.commit()
            return True
        finally:
            cursor.close()
            conn.close()

    def obtener_por_id(self, agenda_id: int) -> Agenda | None:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT id, id_paciente, id_medico, fecha_consulta, estado
                FROM agenda
                WHERE id = :id
            """, {"id": agenda_id})
            row = cursor.fetchone()
            return Agenda(*row) if row else None
        finally:
            cursor.close()
            conn.close()

    def listar(self) -> list[Agenda]:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT id, id_paciente, id_medico, fecha_consulta, estado
                FROM agenda
                ORDER BY fecha_consulta DESC
            """)
            rows = cursor.fetchall()
            return [Agenda(*r) for r in rows]
        finally:
            cursor.close()
            conn.close()

    def actualizar(self, agenda: Agenda) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE agenda
                SET id_paciente=:id_paciente, id_medico=:id_medico, fecha_consulta=:fecha_consulta, estado=:estado
                WHERE id=:id
            """, {
                "id_paciente": agenda.id_paciente,
                "id_medico": agenda.id_medico,
                "fecha_consulta": agenda.fecha_consulta,
                "estado": agenda.estado,
                "id": agenda.id
            })
            conn.commit()
            return True
        finally:
            cursor.close()
            conn.close()

    def eliminar(self, agenda_id: int) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM agenda WHERE id=:id", {"id": agenda_id})
            conn.commit()
            return True
        finally:
            cursor.close()
            conn.close()
    