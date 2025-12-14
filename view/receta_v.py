# view/receta_v.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from middleware.auth import login_required
from controller.receta_c import RecetaController

receta_bp = Blueprint("receta", __name__)
controller = RecetaController()

# --- Listar recetas ---
@receta_bp.route("/recetas", methods=["GET"])
@login_required
def listar_recetas():
    recetas = controller.listar()
    return render_template("receta/listar_recetas.html", recetas=recetas)

# --- Crear receta ---
@receta_bp.route("/receta/nueva", methods=["GET", "POST"])
@login_required
def crear_receta():
    if request.method == "POST":
        receta_data = {
            "id_paciente": request.form.get("id_paciente"),
            "id_medico": request.form.get("id_medico"),
            "descripcion": request.form.get("descripcion"),
            "medicamentos_recetados": request.form.get("medicamentos_recetados"),
            "costo_clp": request.form.get("costo_clp"),
            "fecha": request.form.get("fecha")
        }
        success = controller.crear_receta(receta_data)
        flash("Receta creada correctamente" if success else "Error al crear receta")
        return redirect(url_for("receta.listar_recetas"))

    return render_template("receta/crear_receta.html")


@receta_bp.route("/receta/editar/<int:id_receta>", methods=["GET", "POST"])
@login_required
def editar_receta_action(id_receta):
    receta = controller.obtener_por_id(id_receta)
    if not receta:
        flash("Receta no encontrada")
        return redirect(url_for("receta.listar_recetas"))

    if request.method == "POST":
        receta.descripcion = request.form.get("descripcion", receta.descripcion)
        receta.medicamentos_recetados = request.form.get("medicamentos_recetados", receta.medicamentos_recetados)
        receta.costo_clp = request.form.get("costo_clp", receta.costo_clp)
        receta.fecha = request.form.get("fecha", receta.fecha)

        ok = controller.actualizar_receta(receta)
        flash("Receta actualizada" if ok else "Error al actualizar receta")
        return redirect(url_for("receta.listar_recetas"))

    return render_template("receta/editar_receta.html", receta=receta)

# --- Eliminar receta ---
@receta_bp.route("/receta/eliminar/<int:id_receta>", methods=["POST"])
@login_required
def eliminar_receta(id_receta):
    success = controller.eliminar(id_receta)
    flash("Receta eliminada correctamente" if success else "Error al eliminar receta")
    return redirect(url_for("receta.listar_recetas"))
