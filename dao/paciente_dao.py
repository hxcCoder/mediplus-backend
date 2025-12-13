from models.paciente import Paciente
from db.connection import get_connection

class PacienteDAO:

    @staticmethod
    def crear(paciente: Paciente):
        conn = get_connection()
        cursor = conn.cursor()

        # Se asume que usuario ya fue creado
        sql = """
        INSERT INTO paciente (
            id_usuario, comuna, fecha_primera_visita
        ) VALUES (
            :id_usuario, :comuna, :fecha_primera_visita
        )
        """

        cursor.execute(sql, {
            "id_usuario": paciente.id,
            "comuna": paciente.comuna,
            "fecha_primera_visita": paciente.fecha_primera_visita
        })

        conn.commit()
        cursor.close()
        conn.close()

    # ----------------------------

    @staticmethod
    def obtener_por_id_usuario(id_usuario):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
        SELECT u.id, u.nombre_usuario, u.clave, u.nombre, u.apellido,
               u.fecha_nacimiento, u.telefono, u.email, u.tipo,
               p.comuna, p.fecha_primera_visita
        FROM usuario u
        JOIN paciente p ON p.id_usuario = u.id
        WHERE u.id = :id
        """

        cursor.execute(sql, {"id": id_usuario})
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row:
            return Paciente(
                id=row[0],
                nombre_usuario=row[1],
                clave=row[2],
                nombre=row[3],
                apellido=row[4],
                fecha_nacimiento=row[5],
                telefono=row[6],
                email=row[7],
                tipo=row[8],
                comuna=row[9],
                fecha_primera_visita=row[10]
            )
        return None
