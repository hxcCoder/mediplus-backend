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
        flash("Debes completar todos los campos")
        return redirect(url_for("login.login_form"))

    usuario = auth_controller.login(nombre_usuario, clave)
    if not usuario:
        flash("Usuario o contraseña incorrectos")
        return redirect(url_for("login.login_form"))

    # Guardar datos en session
    session["user_id"] = usuario.id
    session["username"] = usuario.nombre_usuario
    session["tipo"] = usuario.tipo
    session["user"] = {"id": usuario.id, "username": usuario.nombre_usuario, "tipo": usuario.tipo}

    # Redirigir según tipo
    tipo_lower = usuario.tipo.lower()
    if tipo_lower == "admin":
        return redirect(url_for("administrador.menu_admin"))
    elif tipo_lower == "medico":
        return redirect(url_for("menu_medico.menu"))
    elif tipo_lower == "paciente":
        return redirect(url_for("menu_paciente.menu"))
    else:
        flash("Tipo de usuario desconocido")
        return redirect(url_for("login.login_form"))

@login_bp.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada correctamente")
    return redirect(url_for("login.login_form"))
