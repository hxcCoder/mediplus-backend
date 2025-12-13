# dao/insumo_dao.py
from db.connection import get_connection
from models.insumo import Insumo


class InsumoDAO:

    def listar(self):
        conn = cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT id, nombre, tipo, stock, costo_usd
                FROM insumo
                ORDER BY nombre
            """)
            rows = cur.fetchall()
            return [Insumo(*r) for r in rows]
        finally:
            if cur: cur.close()
            if conn: conn.close()

    def obtener_por_id(self, insumo_id):
        conn = cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT id, nombre, tipo, stock, costo_usd
                FROM insumo
                WHERE id = :id
            """, {"id": insumo_id})
            row = cur.fetchone()
            return Insumo(*row) if row else None
        finally:
            if cur: cur.close()
            if conn: conn.close()

    def crear(self, insumo: Insumo):
        conn = cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO insumo (nombre, tipo, stock, costo_usd)
                VALUES (:1, :2, :3, :4)
            """, [insumo.nombre, insumo.tipo, insumo.stock, insumo.costo_usd])
            conn.commit()
            return True
        finally:
            if cur: cur.close()
            if conn: conn.close()

    def actualizar(self, insumo: Insumo):
        conn = cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                UPDATE insumo
                SET nombre=:1, tipo=:2, stock=:3, costo_usd=:4
                WHERE id=:5
            """, [insumo.nombre, insumo.tipo, insumo.stock, insumo.costo_usd, insumo.id])
            conn.commit()
            return True
        finally:
            if cur: cur.close()
            if conn: conn.close()

    def eliminar(self, insumo_id):
        conn = cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM insumo WHERE id=:id", {"id": insumo_id})
            conn.commit()
            return True
        finally:
            if cur: cur.close()
            if conn: conn.close()
