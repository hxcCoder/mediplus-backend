import json
from pathlib import Path
from controller.auth_c import AuthController
from models.usuario import Usuario

auth_controller = AuthController()

# Ruta al JSON
json_path = Path(__file__).parent / "scripts.json"

def cargar_usuarios_desde_json():
    if not json_path.exists():
        print("No se encontró scripts.json")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        try:
            usuarios_data = json.load(f)
        except json.JSONDecodeError:
            print("JSON vacío o inválido")
            return

    for u in usuarios_data:
        # Crear objeto Usuario
        usuario = Usuario(
            nombre_usuario=u.get("nombre_usuario"),
            clave=u.get("clave"),
            nombre=u.get("nombre"),
            apellido=u.get("apellido"),
            fecha_nacimiento=u.get("fecha_nacimiento"),
            telefono=u.get("telefono"),
            email=u.get("email"),
            tipo=u.get("tipo")
        )

        # Intentar registrar usuario
        try:
            success = auth_controller.registrar_usuario(usuario)
            if success:
                print(f"Usuario '{usuario.nombre_usuario}' registrado correctamente")
            else:
                print(f"Usuario '{usuario.nombre_usuario}' ya existe o hubo un error")
        except Exception as e:
            print(f"Error registrando '{usuario.nombre_usuario}': {e}")


if __name__ == "__main__":
    cargar_usuarios_desde_json()
