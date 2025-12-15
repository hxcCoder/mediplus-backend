from flask import Blueprint, render_template, request, redirect, url_for, flash
from controller.insumo_c import InsumoController

insumo_bp = Blueprint("insumo_bp", __name__, template_folder="../templates")

controller = InsumoController()

@insumo_bp.route("/insumos")
def listar_insumos():
    insumos = controller.listar_insumos()
    return render_template("insumos/listar.html", insumos=insumos)

@insumo_bp.route("/insumos/crear", methods=["GET", "POST"])
def crear_insumo():
    if request.method == "POST":
        nombre = request.form.get("nombre", "")
        tipo = request.form.get("tipo", "")
        stock = request.form.get("stock", "0")
        costo_usd = request.form.get("costo_usd", "0")

        try:
            stock = int(stock)
        except ValueError:
            stock = 0
        try:
            costo_usd = float(costo_usd)
        except ValueError:
            costo_usd = 0.0

        if controller.crear_insumo(nombre, tipo, stock, costo_usd):
            flash("Insumo creado correctamente", "success")
            return redirect(url_for("insumo_bp.listar_insumos"))
        else:
            flash("Error al crear insumo", "danger")

    return render_template("insumos/crear.html")

@insumo_bp.route("/insumos/editar/<int:insumo_id>", methods=["GET", "POST"])
def editar_insumo(insumo_id):
    insumo = controller.obtener_insumo_por_id(insumo_id)
    if not insumo:
        flash("Insumo no encontrado", "warning")
        return redirect(url_for("insumo_bp.listar_insumos"))

    if request.method == "POST":
        nombre = request.form.get("nombre", "")
        tipo = request.form.get("tipo", "")
        stock = request.form.get("stock", "0")
        costo_usd = request.form.get("costo_usd", "0")

        try:
            stock = int(stock)
        except ValueError:
            stock = 0
        try:
            costo_usd = float(costo_usd)
        except ValueError:
            costo_usd = 0.0

        if controller.actualizar_insumo(insumo_id, nombre, tipo, stock, costo_usd):
            flash("Insumo actualizado correctamente", "success")
            return redirect(url_for("insumo_bp.listar_insumos"))
        else:
            flash("Error al actualizar insumo", "danger")

    return render_template("insumos/editar.html", insumo=insumo)

@insumo_bp.route("/insumos/eliminar/<int:insumo_id>", methods=["POST"])
def eliminar_insumo(insumo_id):
    if controller.eliminar_insumo(insumo_id):
        flash("Insumo eliminado correctamente", "success")
    else:
        flash("Error al eliminar insumo", "danger")
    return redirect(url_for("insumo_bp.listar_insumos"))
