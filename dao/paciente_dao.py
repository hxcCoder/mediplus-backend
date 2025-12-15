from db.connection import get_connection
from models.paciente import Paciente
from dao.usuario_dao import UsuarioDAO
import bcrypt

class PacienteDAO:

    def crear(self, paciente: Paciente) -> bool:
        if not paciente.clave:
            raise ValueError("La contraseña no puede ser None.")

        # Crear usuario
        usuario_dao = UsuarioDAO()
        paciente.tipo = "PACIENTE"
        hashed = bcrypt.hashpw(paciente.clave.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        paciente.clave = hashed
        if not usuario_dao.crear(paciente):
            return False

        # Obtener ID generado
        creado = usuario_dao.obtener_por_nombre_usuario(paciente.nombre_usuario)
        if not creado:
            return False

        # Insertar en tabla PACIENTE
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO PACIENTE (id, comuna, fecha_primera_visita)
            VALUES (:1, :2, :3)
        """
        cursor.execute(sql, [
            creado.id,
            paciente.comuna,
            paciente.fecha_primera_visita
        ])
        conn.commit()
        cursor.close()
        conn.close()
        return True

    def obtener_por_id(self, paciente_id: int) -> Paciente | None:
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            SELECT u.id, u.nombre_usuario, u.clave, u.nombre, u.apellido,
                   u.fecha_nacimiento, u.telefono, u.email, u.tipo,
                   p.comuna, p.fecha_primera_visita
            FROM USUARIO u
            JOIN PACIENTE p ON u.id = p.id
            WHERE u.id = :id
        """
        cursor.execute(sql, {"id": paciente_id})
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

    def listar(self) -> list[Paciente]:
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            SELECT u.id, u.nombre_usuario, u.clave, u.nombre, u.apellido,
                   u.fecha_nacimiento, u.telefono, u.email, u.tipo,
                   p.comuna, p.fecha_primera_visita
            FROM USUARIO u
            JOIN PACIENTE p ON u.id = p.id
            WHERE u.tipo='PACIENTE'
            ORDER BY u.id
        """
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [
            Paciente(
                id=r[0],
                nombre_usuario=r[1],
                clave=r[2],
                nombre=r[3],
                apellido=r[4],
                fecha_nacimiento=r[5],
                telefono=r[6],
                email=r[7],
                tipo=r[8],
                comuna=r[9],
                fecha_primera_visita=r[10]
            ) for r in rows
        ]

    def actualizar(self, paciente: Paciente) -> bool:
        # Actualizar USUARIO
        usuario_dao = UsuarioDAO()
        if not usuario_dao.actualizar(paciente):
            return False

        # Actualizar PACIENTE
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            UPDATE PACIENTE
            SET comuna=:1, fecha_primera_visita=:2
            WHERE id=:3
        """
        cursor.execute(sql, [
            paciente.comuna,
            paciente.fecha_primera_visita,
            paciente.id
        ])
        conn.commit()
        cursor.close()
        conn.close()
        return True

    def eliminar(self, paciente_id: int) -> bool:
        # Eliminar de USUARIO, PACIENTE se borra por ON DELETE CASCADE
        usuario_dao = UsuarioDAO()
        return usuario_dao.eliminar(paciente_id)
