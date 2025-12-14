# dao/paciente_dao.py
from db.connection import get_connection
from models.paciente import Paciente
import bcrypt

class PacienteDAO:

    def crear(self, paciente: Paciente):
        if not paciente.clave:
            raise ValueError("La clave no puede ser None.")

        conn = get_connection()
        cursor = conn.cursor()

        hashed = bcrypt.hashpw(paciente.clave.encode("utf-8"), bcrypt.gensalt())

        sql = """
            INSERT INTO usuario 
            (nombre_usuario, clave, nombre, apellido, fecha_nacimiento, telefono, email, tipo, comuna, fecha_primera_visita)
            VALUES (:1, :2, :3, :4, :5, :6, :7, 'paciente', :8, :9)
        """

        cursor.execute(sql, [
            paciente.nombre_usuario,
            hashed,
            paciente.nombre,
            paciente.apellido,
            paciente.fecha_nacimiento,
            paciente.telefono,
            paciente.email,
            paciente.comuna,
            paciente.fecha_primera_visita
        ])

        conn.commit()
        cursor.close()
        conn.close()
        return True

    def obtener_por_id(self, paciente_id: int):
        conn = get_connection()
        cursor = conn.cursor()

        sql = "SELECT * FROM usuario WHERE id = :id AND tipo='paciente'"
        cursor.execute(sql, {"id": paciente_id})
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row:
            return Paciente(**{
                "id": row[0],
                "nombre_usuario": row[1],
                "clave": row[2],
                "nombre": row[3],
                "apellido": row[4],
                "fecha_nacimiento": row[5],
                "telefono": row[6],
                "email": row[7],
                "tipo": row[8],
                "comuna": row[9],
                "fecha_primera_visita": row[10]
            })
        return None

    def listar(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM usuario WHERE tipo='paciente' ORDER BY id")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        pacientes = []
        for r in rows:
            pacientes.append(Paciente(**{
                "id": r[0],
                "nombre_usuario": r[1],
                "clave": r[2],
                "nombre": r[3],
                "apellido": r[4],
                "fecha_nacimiento": r[5],
                "telefono": r[6],
                "email": r[7],
                "tipo": r[8],
                "comuna": r[9],
                "fecha_primera_visita": r[10]
            }))
        return pacientes

    def actualizar(self, paciente: Paciente):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            UPDATE usuario
            SET nombre_usuario=:1, nombre=:2, apellido=:3,
                fecha_nacimiento=:4, telefono=:5, email=:6,
                comuna=:7, fecha_primera_visita=:8
            WHERE id=:9 AND tipo='paciente'
        """

        cursor.execute(sql, [
            paciente.nombre_usuario,
            paciente.nombre,
            paciente.apellido,
            paciente.fecha_nacimiento,
            paciente.telefono,
            paciente.email,
            paciente.comuna,
            paciente.fecha_primera_visita,
            paciente.id
        ])

        conn.commit()
        cursor.close()
        conn.close()
        return True

    def eliminar(self, paciente_id: int):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuario WHERE id=:id AND tipo='paciente'", {"id": paciente_id})
        conn.commit()
        cursor.close()
        conn.close()
        return True
