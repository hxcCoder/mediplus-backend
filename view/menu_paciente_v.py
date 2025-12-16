from flask import Blueprint, render_template, session, redirect, url_for, flash

menu_paciente_bp = Blueprint("menu_paciente", __name__, url_prefix="/paciente")

@menu_paciente_bp.route("/menu", methods=["GET"])
def menu():
    # Validar sesión y tipo de usuario
    if "usuario_id" not in session or session.get("usuario_tipo") != "PACIENTE":
        flash("Acceso denegado")
        return redirect(url_for("login.login_form"))

    # Datos del paciente desde session
    username = session.get("usuario_nombre")

    return render_template("menus/menu_paciente.html", username=username)
