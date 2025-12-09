from db.connection import get_connection
from models.insumo import Insumo

class InsumoController:

    # Crear insumo
    def crear(self, insumo: Insumo):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            INSERT INTO insumo (nombre, tipo, stock, costo_usd)
            VALUES (:1, :2, :3, :4)
        """

        cursor.execute(sql, [
            insumo.nombre,
            insumo.tipo,
            insumo.stock,
            insumo.costo_usd
        ])

        conn.commit()
        cursor.close()
        conn.close()
        return True

    # Obtener insumo por ID
    def obtener_por_id(self, insumo_id):
        conn = get_connection()
        cursor = conn.cursor()

        sql = "SELECT * FROM insumo WHERE id = :id"
        cursor.execute(sql, {"id": insumo_id})
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row:
            return Insumo(*row)
        return None

    # Listar todos los insumos
    def listar(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM insumo ORDER BY id")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()
        return [Insumo(*r) for r in rows]

    # Actualizar insumo
    def actualizar(self, insumo: Insumo):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            UPDATE insumo
            SET nombre=:1, tipo=:2, stock=:3, costo_usd=:4
            WHERE id=:5
        """

        cursor.execute(sql, [
            insumo.nombre,
            insumo.tipo,
            insumo.stock,
            insumo.costo_usd,
            insumo.id
        ])

        conn.commit()
        cursor.close()
        conn.close()
        return True

    # Eliminar insumo
    def eliminar(self, insumo_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM insumo WHERE id=:id", {"id": insumo_id})
        conn.commit()

        cursor.close()
        conn.close()
        return True
