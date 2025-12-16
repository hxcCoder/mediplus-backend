# dao/consulta_dao.py
from db.connection import get_connection
from models.consulta import Consulta
from typing import List, Optional

class ConsultaDAO:
    def crear(self, consulta: Consulta) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO CONSULTA 
                (id, id_paciente, id_medico, id_receta, fecha, comentarios, valor)
                VALUES (CONSULTA_SEQ.NEXTVAL, :id_paciente, :id_medico, :id_receta, :fecha, :comentarios, :valor)
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
        except Exception as e:
            conn.rollback()
            print("Error al crear consulta:", e)
            return False
        finally:
            cursor.close()
            conn.close()

    def listar_por_medico(self, id_medico: int) -> List[Consulta]:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT id, id_paciente, id_medico, id_receta, fecha, comentarios, valor
                FROM CONSULTA
                WHERE id_medico = :id_medico
                ORDER BY fecha DESC
            """, {"id_medico": id_medico})
            rows = cursor.fetchall()
            return [Consulta(*r) for r in rows]
        finally:
            cursor.close()
            conn.close()

    def obtener_por_id(self, consulta_id: int) -> Optional[Consulta]:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT id, id_paciente, id_medico, id_receta, fecha, comentarios, valor
                FROM CONSULTA
                WHERE id = :id
            """, {"id": consulta_id})
            row = cursor.fetchone()
            return Consulta(*row) if row else None
        finally:
            cursor.close()
            conn.close()

    def listar(self) -> List[Consulta]:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT id, id_paciente, id_medico, id_receta, fecha, comentarios, valor
                FROM CONSULTA
                ORDER BY fecha DESC
            """)
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
                UPDATE CONSULTA
                SET id_paciente=:id_paciente,
                    id_medico=:id_medico,
                    id_receta=:id_receta,
                    fecha=:fecha,
                    comentarios=:comentarios,
                    valor=:valor
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
        except Exception as e:
            conn.rollback()
            print("Error al actualizar consulta:", e)
            return False
        finally:
            cursor.close()
            conn.close()

    def eliminar(self, consulta_id: int) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM CONSULTA WHERE id=:id", {"id": consulta_id})
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print("Error al eliminar consulta:", e)
            return False
        finally:
            cursor.close()
            conn.close()
