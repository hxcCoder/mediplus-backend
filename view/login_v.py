from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from controller.auth_c import AuthController

login_bp = Blueprint("login", __name__)
auth_controller = AuthController()

@login_bp.route("/login", methods=["GET"])
def login_form():
    return render_template("auth/login.html")

@login_bp.route("/login", methods=["POST"])
def login_action():
    nombre_usuario = request.form.get("nombre_usuario")
    clave = request.form.get("clave")

    if not nombre_usuario or not clave:
        flash("Debes completar todos los campos", "error")
        return redirect(url_for("login.login_form"))

    usuario = auth_controller.login(nombre_usuario, clave)
    if usuario:
        session["usuario_id"] = usuario.id
        session["usuario_nombre"] = usuario.nombre_usuario
        session["usuario_tipo"] = usuario.tipo
        flash(f"Bienvenido, {usuario.nombre_completo()}", "success")

        # Redirige según tipo de usuario
        if usuario.tipo == "ADMIN":
            return redirect(url_for("menu_admin.menu"))
        elif usuario.tipo == "MEDICO":
            return redirect(url_for("menu_medico.menu"))
        else:
            return redirect(url_for("menu_paciente.menu"))

    flash("Usuario o contraseña incorrectos", "error")
    return redirect(url_for("login.login_form"))

@login_bp.route("/logout")
def logout():
    session.clear()
    flash("Has cerrado sesión correctamente", "success")
    return redirect(url_for("login.login_form"))
