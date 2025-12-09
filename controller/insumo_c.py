# insumo_c.py
from db.connection import get_connection  #
from models.insumo import Insumo


class InsumoController:

    # Crear insumo
    def crear(self, insumo: Insumo):
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            sql = """
                INSERT INTO insumo (nombre, tipo, stock, costo_usd)
                VALUES (:1, :2, :3, :4)
            """
            cur.execute(sql, [insumo.nombre, insumo.tipo, insumo.stock, insumo.costo_usd])
            conn.commit()
            return True
        finally:
            if cur:  # type: ignore
                cur.close()
            if conn:  # type: ignore
                conn.close()

    # Obtener insumo por ID
    def obtener_por_id(self, insumo_id):
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            sql = "SELECT * FROM insumo WHERE id=:id"
            cur.execute(sql, {"id": insumo_id})
            row = cur.fetchone()
            if row:
                return Insumo(*row)
            return None
        finally:
            if cur:  # type: ignore
                cur.close()
            if conn:  # type: ignore
                conn.close()

    # Listar todos los insumos
    def listar(self):
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM insumo ORDER BY id")
            rows = cur.fetchall()
            return [Insumo(*r) for r in rows]
        finally:
            if cur:  # type: ignore
                cur.close()
            if conn:  # type: ignore
                conn.close()

    # Actualizar insumo
    def actualizar(self, insumo: Insumo):
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            sql = """
                UPDATE insumo
                SET nombre=:1, tipo=:2, stock=:3, costo_usd=:4
                WHERE id=:5
            """
            cur.execute(sql, [insumo.nombre, insumo.tipo, insumo.stock, insumo.costo_usd, insumo.id])
            conn.commit()
            return True
        finally:
            if cur:  # type: ignore
                cur.close()
            if conn:  # type: ignore
                conn.close()

    # Eliminar insumo
    def eliminar(self, insumo_id):
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM insumo WHERE id=:id", {"id": insumo_id})
            conn.commit()
            return True
        finally:
            if cur:  # type: ignore
                cur.close()
            if conn:  # type: ignore
                conn.close()
