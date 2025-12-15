from db.connection import get_connection
from models.medico import Medico
from dao.usuario_dao import UsuarioDAO
import bcrypt

class MedicoDAO:
    """DAO para la entidad Medico"""

    def crear(self, medico: Medico) -> bool:
        if not medico.clave:
            raise ValueError("La contraseña no puede ser None")

        # Primero insertamos en USUARIO
        usuario_dao = UsuarioDAO()
        medico.tipo = "MEDICO"
        hashed = bcrypt.hashpw(medico.clave.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        medico.clave = hashed
        if not usuario_dao.crear(medico):
            return False

        # Obtener el ID generado
        creado = usuario_dao.obtener_por_nombre_usuario(medico.nombre_usuario)
        if not creado:
            return False

        # Insertar en tabla MEDICO
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO MEDICO (id, especialidad, horario_atencion, fecha_ingreso)
            VALUES (:1, :2, :3, :4)
        """
        cursor.execute(sql, [
            creado.id,
            medico.especialidad,
            medico.horario_atencion,
            medico.fecha_ingreso
        ])
        conn.commit()
        cursor.close()
        conn.close()
        return True

    def obtener_por_id(self, medico_id: int) -> Medico | None:
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            SELECT u.id, u.nombre_usuario, u.clave, u.nombre, u.apellido,
                   u.fecha_nacimiento, u.telefono, u.email, u.tipo,
                   m.especialidad, m.horario_atencion, m.fecha_ingreso
            FROM USUARIO u
            JOIN MEDICO m ON u.id = m.id
            WHERE u.id = :id
        """
        cursor.execute(sql, {"id": medico_id})
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return Medico(
                id=row[0],
                nombre_usuario=row[1],
                clave=row[2],
                nombre=row[3],
                apellido=row[4],
                fecha_nacimiento=row[5],
                telefono=row[6],
                email=row[7],
                tipo=row[8],
                especialidad=row[9],
                horario_atencion=row[10],
                fecha_ingreso=row[11]
            )
        return None

    def listar(self) -> list[Medico]:
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            SELECT u.id, u.nombre_usuario, u.clave, u.nombre, u.apellido,
                   u.fecha_nacimiento, u.telefono, u.email, u.tipo,
                   m.especialidad, m.horario_atencion, m.fecha_ingreso
            FROM USUARIO u
            JOIN MEDICO m ON u.id = m.id
            WHERE u.tipo='MEDICO'
            ORDER BY u.id
        """
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [
            Medico(
                id=r[0],
                nombre_usuario=r[1],
                clave=r[2],
                nombre=r[3],
                apellido=r[4],
                fecha_nacimiento=r[5],
                telefono=r[6],
                email=r[7],
                tipo=r[8],
                especialidad=r[9],
                horario_atencion=r[10],
                fecha_ingreso=r[11]
            ) for r in rows
        ]

    def actualizar(self, medico: Medico) -> bool:
        # Actualizar USUARIO
        usuario_dao = UsuarioDAO()
        if not usuario_dao.actualizar(medico):
            return False

        # Actualizar MEDICO
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            UPDATE MEDICO
            SET especialidad=:1, horario_atencion=:2, fecha_ingreso=:3
            WHERE id=:4
        """
        cursor.execute(sql, [
            medico.especialidad,
            medico.horario_atencion,
            medico.fecha_ingreso,
            medico.id
        ])
        conn.commit()
        cursor.close()
        conn.close()
        return True

    def eliminar(self, medico_id: int) -> bool:
        # Solo eliminar de USUARIO, MEDICO se borra por ON DELETE CASCADE
        usuario_dao = UsuarioDAO()
        return usuario_dao.eliminar(medico_id)
