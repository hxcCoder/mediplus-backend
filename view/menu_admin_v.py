from flask import Blueprint, render_template, session, redirect, url_for, flash
from controller.administrador_c import AdministradorController

menu_admin_bp = Blueprint("menu_admin", __name__, url_prefix="/admin")
admin_ctrl = AdministradorController()

@menu_admin_bp.route("/menu", methods=["GET"])
def menu():
    # Validar sesión y tipo de usuario
    if "usuario_id" not in session or session.get("usuario_tipo") != "ADMIN":
        flash("Acceso denegado")
        return redirect(url_for("login.login_form"))

    # Datos del administrador desde session
    username = session.get("usuario_nombre")

    # Obtener lista de administradores para mostrar en la vista
    admins = admin_ctrl.listar_admins()

    return render_template(
        "administrador/menu_admin.html",
        username=username,
        admins=admins
    )
