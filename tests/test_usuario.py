# test_usuario.py
from models.usuario import Usuario
from controller.usuario_c import UsuarioController

def main():
    controller = UsuarioController()

    print("=== CREANDO USUARIO ===")
    nuevo_usuario = Usuario(
        nombre_usuario="benjamin123",
        clave="MiClaveSegura123",  # Debe hasharse en utils/security.py antes de guardar
        nombre="Benjamin",
        apellido="Millalonco",
        email="benjamin@test.com",
        telefono="123456789",
        tipo="PACIENTE"
    )
    exito = controller.crear_usuario(nuevo_usuario)
    print("Creación exitosa:", exito)

    print("\n=== LISTAR USUARIOS ===")
    usuarios = controller.listar_usuarios()
    for u in usuarios:
        print(f"ID: {u.id}, Nombre: {u.nombre_completo()}, Usuario: {u.nombre_usuario}, Tipo: {u.tipo}")

    print("\n=== LOGIN USUARIO ===")
    login = controller.login_usuario("benjamin123", "MiClaveSegura123")
    if login:
        print("Login exitoso:", login.nombre_completo())
    else:
        print("Login fallido")

    print("\n=== ACTUALIZAR USUARIO ===")
    if usuarios:
        usuario_a_actualizar = usuarios[-1]
        usuario_a_actualizar.nombre = "Benja"
        exito = controller.actualizar_usuario(usuario_a_actualizar)
        print("Actualización exitosa:", exito)

    print("\n=== ELIMINAR USUARIO ===")
    if usuarios:
        usuario_a_eliminar = usuarios[-1]
        exito = controller.eliminar_usuario(usuario_a_eliminar.id)
        print("Eliminación exitosa:", exito)

if __name__ == "__main__":
    main()
