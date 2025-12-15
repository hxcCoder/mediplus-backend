# controller/usuario_c.py
from typing import Optional, List
from models.usuario import Usuario
from dao.usuario_dao import UsuarioDAO

class UsuarioController:
    """Controller para manejar la lógica de Usuario, sin depender de Flask."""

    def __init__(self, dao: Optional[UsuarioDAO] = None):
        # Permite inyectar un DAO distinto (por ejemplo, para pruebas)
        self.dao = dao or UsuarioDAO()

    def crear_usuario(self, usuario: Usuario) -> bool:
        """Crea un usuario nuevo. Devuelve True si se creó correctamente."""
        if not usuario.nombre_usuario or not usuario.clave:
            print("[Error] Nombre de usuario y clave son obligatorios")
            return False
        # Podria agregar más validaciones aqui
        return self.dao.crear(usuario)

    def obtener_usuario_por_id(self, usuario_id: int) -> Optional[Usuario]:
        """Devuelve un usuario por su ID o None si no existe."""
        return self.dao.obtener_por_id(usuario_id)

    def obtener_usuario_por_nombre(self, nombre_usuario: str) -> Optional[Usuario]:
        """Devuelve un usuario por su nombre de usuario o None."""
        return self.dao.obtener_por_nombre_usuario(nombre_usuario)

    def login_usuario(self, nombre_usuario: str, clave: str) -> Optional[Usuario]:
        """Intenta autenticar a un usuario. Devuelve Usuario si éxito, None si falla."""
        if not nombre_usuario or not clave:
            print("[Error] Nombre de usuario y clave son requeridos")
            return None
        return self.dao.login(nombre_usuario, clave)

    def listar_usuarios(self) -> List[Usuario]:
        """Devuelve todos los usuarios como lista de objetos Usuario."""
        return self.dao.listar()

    def actualizar_usuario(self, usuario: Usuario) -> bool:
        """Actualiza un usuario existente. Devuelve True si se actualizó correctamente."""
        if not usuario.id:
            print("[Error] El ID del usuario es obligatorio para actualizar")
            return False
        return self.dao.actualizar(usuario)

    def eliminar_usuario(self, usuario_id: int) -> bool:
        """Elimina un usuario por ID. Devuelve True si se eliminó correctamente."""
        return self.dao.eliminar(usuario_id)
