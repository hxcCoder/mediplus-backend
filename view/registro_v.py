from flask import Blueprint, render_template, request, redirect, flash
from controller.auth_c import AuthController
from models.usuario import Usuario

registro_bp = Blueprint("registro", __name__)
auth_controller = AuthController()  # instancia del controlador

# --- Mostrar formulario de registro ---
@registro_bp.route("/register", methods=["GET"])
def register_form():
    return render_template("register.html")  # Debes crear templates/register.html

# --- Procesar registro desde formulario ---
@registro_bp.route("/register", methods=["POST"])
def register_action():
    # Obtener datos del formulario
    nombre_usuario = request.form.get("nombre_usuario")
    clave = request.form.get("clave")
    nombre = request.form.get("nombre")
    apellido = request.form.get("apellido")
    fecha_nacimiento = request.form.get("fecha_nacimiento")
    telefono = request.form.get("telefono")
    email = request.form.get("email")
    tipo = request.form.get("tipo")  # paciente / medico / admin

    # Validación mínima
    if not nombre_usuario or not clave:
        flash("Nombre de usuario y contraseña son obligatorios")
        return redirect("/register")

    # Crear objeto Usuario
    usuario = Usuario(
        nombre_usuario=nombre_usuario,
        clave=clave,
        nombre=nombre,
        apellido=apellido,
        fecha_nacimiento=fecha_nacimiento,
        telefono=telefono,
        email=email,
        tipo=tipo
    )

    # Llamar al controlador
    success = auth_controller.registrar_usuario(usuario)

    if success:
        flash("Usuario registrado correctamente")
        return redirect("/login")
    else:
        flash("Error al registrar usuario. Intente nuevamente.")
        return redirect("/register")
