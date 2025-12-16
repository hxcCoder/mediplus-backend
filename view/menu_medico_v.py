from flask import Blueprint, render_template, session, redirect, url_for, flash

menu_medico_bp = Blueprint("menu_medico", __name__, url_prefix="/medico")

@menu_medico_bp.route("/menu")
def menu():
    # Verificar sesión y rol
    if 'usuario_nombre' not in session or session.get('usuario_tipo') != 'MEDICO':
        flash("Debes iniciar sesión como médico", "error")
        return redirect(url_for("login.login_form"))

    return render_template("menus/menu_medico.html")
