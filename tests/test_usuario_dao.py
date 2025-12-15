from dao.usuario_dao import UsuarioDAO

dao = UsuarioDAO()
usuarios = dao.listar()

print("Usuarios encontrados:", len(usuarios))
for u in usuarios:
    print(u)
