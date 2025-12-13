from flask import Blueprint, jsonify
from middleware.auth import login_required, admin_required
from controller.insumo_c import InsumoController

insumo_bp = Blueprint("insumo", __name__, url_prefix="/insumos")
controller = InsumoController()


@insumo_bp.route("/", methods=["GET"])
@login_required
def listar_insumos():
    insumos = controller.listar()
    return jsonify([i.to_dict() for i in insumos]), 200


@insumo_bp.route("/", methods=["POST"])
@admin_required
def crear_insumo():
    return jsonify({"ok": True})
