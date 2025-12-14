# view/menu_admin_v.py
from flask import Blueprint, render_template, session, redirect, url_for, flash
from controller.administrador_c import AdministradorController

# Blueprint para el menú de administrador
menu_admin_bp = Blueprint("menu_admin", __name__, url_prefix="/admin")

# Instancia del controller
admin_ctrl = AdministradorController()

# --- Ruta principal del menú administrador ---
@menu_admin_bp.route("/menu", methods=["GET"])
def menu():
    # Validar sesión y tipo de usuario
    if "user_id" not in session or session.get("tipo") != "admin":
        flash("Acceso denegado")
        return redirect(url_for("login.login_form"))

    # Obtener datos del administrador desde session
    username = session.get("username")

    # Obtener lista de administradores para mostrar en la vista
    admins = admin_ctrl.listar_admins()

    return render_template(
        "administrador/menu_admin.html",
        username=username,
        admins=admins
    )
