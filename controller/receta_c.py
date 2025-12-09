from db.connection import get_connection
from models.receta import Receta


class RecetaController:

    # Crear receta
    def crear(self, receta: Receta):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            INSERT INTO receta (id_paciente, id_medico, descripcion, fecha)
            VALUES (:1, :2, :3, :4)
        """

        cursor.execute(sql, [
            receta.id_paciente,
            receta.id_medico,
            receta.descripcion,
            receta.fecha
        ])

        conn.commit()
        cursor.close()
        conn.close()
        return True

    # Obtener receta por ID
    def obtener_por_id(self, receta_id):
        conn = get_connection()
        cursor = conn.cursor()

        sql = "SELECT * FROM receta WHERE id = :id"
        cursor.execute(sql, {"id": receta_id})
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row:
            return Receta(*row)
        return None

    # Listar todas las recetas
    def listar(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM receta ORDER BY id")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return [Receta(*r) for r in rows]

    # Actualizar receta
    def actualizar(self, receta: Receta):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            UPDATE receta
            SET id_paciente=:1, id_medico=:2, descripcion=:3, fecha=:4
            WHERE id=:5
        """

        cursor.execute(sql, [
            receta.id_paciente,
            receta.id_medico,
            receta.descripcion,
            receta.fecha,
            receta.id
        ])

        conn.commit()
        cursor.close()
        conn.close()
        return True

    # Eliminar receta
    def eliminar(self, receta_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM receta WHERE id=:id", {"id": receta_id})
        conn.commit()

        cursor.close()
        conn.close()
        return True
