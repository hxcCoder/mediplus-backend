from flask import Blueprint, render_template, session, redirect, url_for, flash

menu_paciente_bp = Blueprint("menu_paciente", __name__)


@menu_paciente_bp.route("/paciente/menu", methods=["GET"])
def menu():
	if "user_id" not in session or session.get("tipo") != "paciente":
		flash("Acceso denegado")
		return redirect(url_for("login.login_form"))

	username = session.get("username")
	return render_template("menu/menu_pacientes.html", username=username)

 