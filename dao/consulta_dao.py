# dao/consulta_dao.py
from db.connection import get_connection
from models.consulta import Consulta

class ConsultaDAO:

    # Crear consulta
    def crear(self, consulta: Consulta):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            INSERT INTO consulta (id_paciente, id_medico, id_receta, fecha, comentarios, valor)
            VALUES (:1, :2, :3, :4, :5, :6)
        """

        cursor.execute(sql, [
            consulta.id_paciente,
            consulta.id_medico,
            consulta.id_receta,
            consulta.fecha,
            consulta.comentarios,
            consulta.valor
        ])

        conn.commit()
        cursor.close()
        conn.close()
        return True

    # Obtener consulta por ID
    def obtener_por_id(self, consulta_id):
        conn = get_connection()
        cursor = conn.cursor()

        sql = "SELECT * FROM consulta WHERE id = :id"
        cursor.execute(sql, {"id": consulta_id})
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row:
            return Consulta(*row)
        return None

    # Listar todas las consultas
    def listar(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM consulta ORDER BY fecha DESC")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()
        return [Consulta(*r) for r in rows]

    # Actualizar consulta
    def actualizar(self, consulta: Consulta):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            UPDATE consulta
            SET id_paciente=:1, id_medico=:2, id_receta=:3,
                fecha=:4, comentarios=:5, valor=:6
            WHERE id=:7
        """

        cursor.execute(sql, [
            consulta.id_paciente,
            consulta.id_medico,
            consulta.id_receta,
            consulta.fecha,
            consulta.comentarios,
            consulta.valor,
            consulta.id
        ])

        conn.commit()
        cursor.close()
        conn.close()
        return True

    # Eliminar consulta
    def eliminar(self, consulta_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM consulta WHERE id=:id", {"id": consulta_id})
        conn.commit()

        cursor.close()
        conn.close()
        return True
