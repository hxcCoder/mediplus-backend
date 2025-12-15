from flask import Blueprint, render_template, request, redirect, url_for, flash
from controller.receta_c import RecetaController
from models.receta import Receta

receta_bp = Blueprint("receta_bp", __name__, template_folder="../templates")

controller = RecetaController()

@receta_bp.route("/recetas")
def listar_recetas():
    recetas = controller.listar_recetas()
    return render_template("recetas/listar.html", recetas=recetas)

@receta_bp.route("/recetas/crear", methods=["GET", "POST"])
def crear_receta():
    if request.method == "POST":
        try:
            id_paciente = int(request.form.get("id_paciente", "0"))
        except ValueError:
            id_paciente = 0
        try:
            id_medico = int(request.form.get("id_medico", "0"))
        except ValueError:
            id_medico = 0

        descripcion = request.form.get("descripcion", "")
        medicamentos = request.form.get("medicamentos", "")
        try:
            costo_clp = float(request.form.get("costo_clp", "0"))
        except ValueError:
            costo_clp = 0.0
        fecha = request.form.get("fecha", "")

        nueva = Receta(
            id=None,
            id_paciente=id_paciente,
            id_medico=id_medico,
            descripcion=descripcion,
            medicamentos_recetados=medicamentos,
            costo_clp=costo_clp,
            fecha=fecha
        )

        if controller.crear_receta(nueva):
            flash("Receta creada correctamente", "success")
            return redirect(url_for("receta_bp.listar_recetas"))
        else:
            flash("Error al crear receta", "danger")

    return render_template("recetas/crear.html")

@receta_bp.route("/recetas/editar/<int:receta_id>", methods=["GET", "POST"])
def editar_receta(receta_id):
    receta = controller.obtener_receta_por_id(receta_id)
    if not receta:
        flash("Receta no encontrada", "warning")
        return redirect(url_for("receta_bp.listar_recetas"))

    if request.method == "POST":
        receta.descripcion = request.form.get("descripcion", receta.descripcion)
        receta.medicamentos_recetados = request.form.get("medicamentos", receta.medicamentos_recetados)
        
        costo_input = request.form.get("costo_clp")
        if costo_input:
            try:
                receta.costo_clp = float(costo_input)
            except ValueError:
                flash("Costo inválido", "danger")
        
        fecha_input = request.form.get("fecha")
        if fecha_input:
            receta.fecha = fecha_input

        if controller.actualizar_receta(receta):
            flash("Receta actualizada correctamente", "success")
            return redirect(url_for("receta_bp.listar_recetas"))
        else:
            flash("Error al actualizar receta", "danger")

    return render_template("recetas/editar.html", receta=receta)

@receta_bp.route("/recetas/eliminar/<int:receta_id>", methods=["POST"])
def eliminar_receta(receta_id):
    if controller.eliminar_receta(receta_id):
        flash("Receta eliminada correctamente", "success")
    else:
        flash("Error al eliminar receta", "danger")
    return redirect(url_for("receta_bp.listar_recetas"))
