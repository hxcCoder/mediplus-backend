from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from controller.receta_c import RecetaController
from models.receta import Receta

receta_bp = Blueprint("receta_bp", __name__, url_prefix="/recetas")
controller = RecetaController()

# Crear receta
@receta_bp.route("/crear", methods=["GET", "POST"])
def crear_receta():
    if request.method == "POST":
        data = request.form
        receta = Receta(
            id=None,
            id_paciente=int(data["id_paciente"]),
            id_medico=int(data["id_medico"]),
            descripcion=data["descripcion"],
            medicamentos_recetados=data["medicamentos_recetados"],
            costo_clp=int(data["costo_clp"]),
            fecha=data["fecha"]
        )
        if controller.crear_receta(receta):
            flash("Receta creada correctamente", "success")
            return redirect(url_for("receta_bp.listar_recetas"))
        else:
            flash("Error al crear la receta", "error")

    return render_template("recetas/crear_receta.html")

# Listar recetas
@receta_bp.route("/", methods=["GET"])
def listar_recetas():
    recetas = controller.listar_recetas()
    return render_template("recetas/listar_recetas.html", recetas=recetas)

# Obtener receta por ID (JSON)
@receta_bp.route("/<int:id_receta>", methods=["GET"])
def obtener_receta(id_receta):
    receta = controller.obtener_receta_por_id(id_receta)
    if receta:
        return jsonify(receta.__dict__)
    return jsonify({"error": "Receta no encontrada"}), 404

# Actualizar receta
@receta_bp.route("/editar/<int:id_receta>", methods=["GET", "POST"])
def editar_receta(id_receta):
    receta = controller.obtener_receta_por_id(id_receta)
    if not receta:
        flash("Receta no encontrada", "error")
        return redirect(url_for("receta_bp.listar_recetas"))

    if request.method == "POST":
        data = request.form
        receta.id_paciente = int(data["id_paciente"])
        receta.id_medico = int(data["id_medico"])
        receta.descripcion = data["descripcion"]
        receta.medicamentos_recetados = data["medicamentos_recetados"]
        receta.costo_clp = int(data["costo_clp"])
        receta.fecha = data["fecha"]

        if controller.actualizar_receta(receta):
            flash("Receta actualizada correctamente", "success")
            return redirect(url_for("receta_bp.listar_recetas"))
        else:
            flash("Error al actualizar la receta", "error")

    return render_template("editar_receta.html", receta=receta)

# Eliminar receta
@receta_bp.route("/eliminar/<int:id_receta>", methods=["POST"])
def eliminar_receta(id_receta):
    if controller.eliminar_receta(id_receta):
        flash("Receta eliminada correctamente", "success")
    else:
        flash("Error al eliminar la receta", "error")
    return redirect(url_for("receta_bp.listar_recetas"))
