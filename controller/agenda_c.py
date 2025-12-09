# controller/agenda_c.py
from db.connection import get_connection
from models.agenda import Agenda

class AgendaController:

    # Crear agenda
    def crear(self, agenda: Agenda):
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            sql = """
                INSERT INTO agenda (id_paciente, id_medico, fecha_consulta, estado)
                VALUES (:1, :2, :3, :4)
            """
            cur.execute(sql, [agenda.id_paciente, agenda.id_medico, agenda.fecha_consulta, agenda.estado])
            conn.commit()
            return True
        finally:
            if cur:  # type: ignore
                cur.close()
            if conn:  # type: ignore
                conn.close()

    # Obtener agenda por ID
    def obtener_por_id(self, agenda_id):
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            sql = "SELECT * FROM agenda WHERE id=:id"
            cur.execute(sql, {"id": agenda_id})
            row = cur.fetchone()
            if row:
                return Agenda(*row)
            return None
        finally:
            if cur:  # type: ignore
                cur.close()
            if conn:  # type: ignore
                conn.close()

    # Listar todas las agendas
    def listar(self):
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM agenda ORDER BY fecha_consulta")
            rows = cur.fetchall()
            return [Agenda(*r) for r in rows]
        finally:
            if cur:  # type: ignore
                cur.close()
            if conn:  # type: ignore
                conn.close()

    # Actualizar agenda
    def actualizar(self, agenda: Agenda):
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            sql = """
                UPDATE agenda
                SET id_paciente=:1, id_medico=:2, fecha_consulta=:3, estado=:4
                WHERE id=:5
            """
            cur.execute(sql, [agenda.id_paciente, agenda.id_medico, agenda.fecha_consulta, agenda.estado, agenda.id])
            conn.commit()
            return True
        finally:
            if cur:  # type: ignore
                cur.close()
            if conn:  # type: ignore
                conn.close()

    # Eliminar agenda
    def eliminar(self, agenda_id):
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM agenda WHERE id=:id", {"id": agenda_id})
            conn.commit()
            return True
        finally:
            if cur:  # type: ignore
                cur.close()
            if conn:  # type: ignore
                conn.close()
