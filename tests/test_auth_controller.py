from controller.auth_c import AuthController
from models.usuario import Usuario


class FakeDAO:
    def __init__(self):
        self.users = {}

    def obtener_por_nombre_usuario(self, nombre):
        return self.users.get(nombre)

    def crear(self, usuario: Usuario):
        if usuario.nombre_usuario in self.users:
            return False
        usuario.id = len(self.users) + 1
        self.users[usuario.nombre_usuario] = usuario
        return True

    def login(self, nombre_usuario: str, clave: str):
        u = self.users.get(nombre_usuario)
        if not u:
            return None
        from utils.security import check_password
        if check_password(clave, u.clave):
            return u
        return None


def test_register_and_login():
    dao = FakeDAO()
    ctrl = AuthController(dao)

    u = Usuario(nombre_usuario="test1", clave="abc123", nombre="T", apellido="U", tipo="paciente")
    assert ctrl.registrar_usuario(u)

    logged = ctrl.login("test1", "abc123")
    assert logged is not None
    assert logged.nombre_usuario == "test1"

    assert ctrl.login("test1", "wrong") is None
