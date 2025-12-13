from flask import Blueprint, render_template, session, redirect, url_for, flash

menu_medico_bp = Blueprint("menu_medico", __name__)

# --- Ruta principal del menú médico ---
@menu_medico_bp.route("/medico/menu", methods=["GET"])
def menu():
    # Validar sesión y tipo de usuario
    if "user_id" not in session or session.get("tipo") != "medico":
        flash("Acceso denegado")
        return redirect(url_for("login.login_form"))

    # Datos del médico desde session
    username = session.get("username")

    return render_template("menu_medico.html", username=username)
    