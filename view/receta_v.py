from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from dao.receta_dao import RecetaDAO
from models.receta import Receta

receta_bp = Blueprint("receta", __name__)
receta_dao = RecetaDAO()

# --- Listar recetas ---
@receta_bp.route("/recetas", methods=["GET"])
def listar_recetas():
    if "user_id" not in session:
        flash("Debes iniciar sesión")
        return redirect(url_for("login.login_form"))

    recetas = receta_dao.listar_todas()
    return render_template("recetas.html", recetas=recetas)

# --- Crear receta ---
@receta_bp.route("/receta/nueva", methods=["GET", "POST"])
def crear_receta():
    if "user_id" not in session:
        flash("Debes iniciar sesión")
        return redirect(url_for("login.login_form"))

    if request.method == "POST":
        receta = Receta(
            id_paciente=request.form.get("id_paciente"),
            id_medico=request.form.get("id_medico"),
            descripcion=request.form.get("descripcion"),
            medicamentos_recetados=request.form.get("medicamentos_recetados"),
            costo_clp=request.form.get("costo_clp"),
            fecha=request.form.get("fecha")
        )
        success = receta_dao.crear(receta)
        flash("Receta creada correctamente" if success else "Error al crear receta")
        return redirect(url_for("receta.listar_recetas"))

    return render_template("crear_receta.html")

# --- Eliminar receta ---
@receta_bp.route("/receta/eliminar/<int:id_receta>", methods=["POST"])
def eliminar_receta(id_receta):
    if "user_id" not in session:
        flash("Debes iniciar sesión")
        return redirect(url_for("login.login_form"))

    success = receta_dao.eliminar(id_receta)
    flash("Receta eliminada correctamente" if success else "Error al eliminar receta")
    return redirect(url_for("receta.listar_recetas"))
