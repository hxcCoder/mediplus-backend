from flask import Blueprint, render_template, session, redirect, url_for, flash

menu_admin_bp = Blueprint("menu_admin", __name__)

# --- Ruta principal del menú administrador ---
@menu_admin_bp.route("/admin/menu", methods=["GET"])
def menu():
    # Validar sesión y tipo de usuario
    if "user_id" not in session or session.get("tipo") != "admin":
        flash("Acceso denegado")
        return redirect(url_for("login.login_form"))

    # Datos del administrador desde session
    username = session.get("username")

    return render_template("menu_admin.html", username=username)
