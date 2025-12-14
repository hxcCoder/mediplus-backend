from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from middleware.auth import login_required, admin_required
from controller.insumo_c import InsumoController

insumo_bp = Blueprint("insumo", __name__, url_prefix="/insumos")
controller = InsumoController()


@insumo_bp.route("/", methods=["GET"])
@login_required
def listar_insumos():
    insumos = controller.listar()
    # Preferir render template, fallback to JSON
    try:
        return render_template("insumo/listar_insumos.html", insumos=insumos)
    except Exception:
        return jsonify([i.to_dict() for i in insumos]), 200


@insumo_bp.route("/", methods=["POST"])
@admin_required
def crear_insumo():
    data = request.get_json() or {}
    # Permitir formulario o JSON
    if not data:
        data = {
            "nombre": request.form.get("nombre"),
            "tipo": request.form.get("tipo"),
            "stock": int(request.form.get("stock", 0)),
            "costo_usd": float(request.form.get("costo_usd", 0.0))
        }

    ok = controller.crear(data)
    if ok:
        return ("", 201) if request.is_json else redirect(url_for("insumo.listar_insumos"))
    return (jsonify({"error": "No se pudo crear insumo"}), 400) if request.is_json else ("Error", 400)


@insumo_bp.route("/<int:insumo_id>", methods=["PUT"])
@admin_required
def actualizar_insumo(insumo_id):
    data = request.get_json() or {}
    ok = controller.actualizar(insumo_id, data)
    if ok:
        return jsonify({"mensaje": "Insumo actualizado"}), 200
    return jsonify({"error": "No se pudo actualizar"}), 400


@insumo_bp.route("/<int:insumo_id>", methods=["DELETE"])
@admin_required
def eliminar_insumo(insumo_id):
    ok = controller.eliminar(insumo_id)
    if ok:
        return jsonify({"mensaje": "Insumo eliminado"}), 200
    return jsonify({"error": "No se pudo eliminar"}), 400
