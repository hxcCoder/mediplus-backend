from db.connection import get_connection
from models.insumo import Insumo

class InsumoDAO:

    def crear(self, insumo: Insumo) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO insumo (nombre, tipo, stock, costo_usd) VALUES (:1, :2, :3, :4)",
            [insumo.nombre, insumo.tipo, insumo.stock, insumo.costo_usd]
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True

    def obtener_por_id(self, insumo_id: int) -> Insumo | None:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM insumo WHERE id=:id", {"id": insumo_id})
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return Insumo(*row) if row else None

    def listar(self) -> list[Insumo]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM insumo ORDER BY id")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [Insumo(*r) for r in rows]

    def actualizar(self, insumo: Insumo) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE insumo SET nombre=:1, tipo=:2, stock=:3, costo_usd=:4 WHERE id=:5",
            [insumo.nombre, insumo.tipo, insumo.stock, insumo.costo_usd, insumo.id]
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True

    def eliminar(self, insumo_id: int) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM insumo WHERE id=:id", {"id": insumo_id})
        conn.commit()
        cursor.close()
        conn.close()
        return True
