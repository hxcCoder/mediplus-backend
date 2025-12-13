from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from controller.auth_c import AuthController

login_bp = Blueprint("login", __name__)
auth_controller = AuthController()  # Instancia del controlador

# --- Mostrar formulario de login ---
@login_bp.route("/login", methods=["GET"])
def login_form():
    return render_template("login.html")  # templates/login.html

# --- Procesar login ---
@login_bp.route("/login", methods=["POST"])
def login_action():
    nombre_usuario = request.form.get("nombre_usuario")
    clave = request.form.get("clave")

    # Validación mínima
    if not nombre_usuario or not clave:
        flash("Nombre de usuario y contraseña son obligatorios")
        return redirect("/login")

    # Llamar al controlador
    usuario = auth_controller.login(nombre_usuario, clave)

    if usuario:
        # Guardar info en session
        session["user_id"] = usuario.id
        session["username"] = usuario.nombre_usuario
        session["tipo"] = usuario.tipo

        flash(f"Bienvenido {usuario.nombre}")
        # Redirigir según tipo de usuario
        if usuario.tipo == "admin":
            return redirect(url_for("menu_admin.menu"))
        elif usuario.tipo == "medico":
            return redirect(url_for("menu_medico.menu"))
        elif usuario.tipo == "paciente":
            return redirect(url_for("menu_paciente.menu"))
        else:
            flash("Tipo de usuario desconocido")
            return redirect("/login")
    else:
        flash("Usuario o contraseña incorrectos")
        return redirect("/login")

# --- Logout ---
@login_bp.route("/logout", methods=["GET"])
def logout():
    session.clear()
    flash("Sesión cerrada correctamente")
    return redirect("/login")
