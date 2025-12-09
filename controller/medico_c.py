# controllers/medico_controller.py
from db.connection import get_connection
from models.usuario import Usuario
import bcrypt

class MedicoController:

    # Crear médico
    def crear_medico(self, medico: Usuario):
        if not medico.clave:
            raise ValueError("La clave no puede ser None.")

        conn = get_connection()
        cursor = conn.cursor()

        hashed = bcrypt.hashpw(medico.clave.encode("utf-8"), bcrypt.gensalt())

        sql = """
            INSERT INTO usuario 
            (nombre_usuario, clave, nombre, apellido, fecha_nacimiento, telefono, email, tipo, especialidad)
            VALUES (:1, :2, :3, :4, :5, :6, :7, 'medico', :8)
        """

        cursor.execute(sql, [
            medico.nombre_usuario,
            hashed,
            medico.nombre,
            medico.apellido,
            medico.fecha_nacimiento,
            medico.telefono,
            medico.email,
            getattr(medico, "especialidad", None)
        ])
        conn.commit()
        cursor.close()
        conn.close()
        return True

    # Obtener médico por ID
    def obtener_por_id(self, medico_id):
        conn = get_connection()
        cursor = conn.cursor()

        sql = "SELECT * FROM usuario WHERE id = :id AND tipo='medico'"
        cursor.execute(sql, {"id": medico_id})
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row:
            return Usuario(**{
                "id": row[0],
                "nombre_usuario": row[1],
                "clave": row[2],
                "nombre": row[3],
                "apellido": row[4],
                "fecha_nacimiento": row[5],
                "telefono": row[6],
                "email": row[7],
                "tipo": row[8],
                "especialidad": row[9]
            })
        return None

    # Listar todos los médicos
    def listar(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM usuario WHERE tipo='medico' ORDER BY id")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        medicos = []
        for r in rows:
            medicos.append(Usuario(**{
                "id": r[0],
                "nombre_usuario": r[1],
                "clave": r[2],
                "nombre": r[3],
                "apellido": r[4],
                "fecha_nacimiento": r[5],
                "telefono": r[6],
                "email": r[7],
                "tipo": r[8],
                "especialidad": r[9]
            }))
        return medicos

    # Actualizar médico
    def actualizar_medico(self, medico: Usuario):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            UPDATE usuario
            SET nombre_usuario=:1, nombre=:2, apellido=:3,
                fecha_nacimiento=:4, telefono=:5, email=:6,
                especialidad=:7
            WHERE id=:8 AND tipo='medico'
        """

        cursor.execute(sql, [
            medico.nombre_usuario,
            medico.nombre,
            medico.apellido,
            medico.fecha_nacimiento,
            medico.telefono,
            medico.email,
            getattr(medico, "especialidad", None),
            medico.id
        ])
        conn.commit()
        cursor.close()
        conn.close()
        return True

    # Eliminar médico
    def eliminar(self, medico_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM usuario WHERE id=:id AND tipo='medico'", {"id": medico_id})
        conn.commit()

        cursor.close()
        conn.close()
        return True
