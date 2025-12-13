# views/agenda_v.py
from flask import Blueprint, request, jsonify
from controller.agenda_c import AgendaController
from models.agenda import Agenda

agenda_bp = Blueprint("agenda", __name__)
controller = AgendaController()

@agenda_bp.route("/agenda", methods=["POST"])
def crear_agenda():
    data = request.json or {}

    try:
        agenda = Agenda(
            id=None,
            id_paciente=data["id_paciente"],
            id_medico=data["id_medico"],
            fecha_consulta=data["fecha_consulta"],
            estado=data.get("estado", "pendiente")
        )
        controller.crear(agenda)
        return jsonify({"ok": True, "mensaje": "agenda creada"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@agenda_bp.route("/agenda", methods=["GET"])
def listar_agendas():
    agendas = controller.listar()
    return jsonify([a.__dict__ for a in agendas])


@agenda_bp.route("/agenda/<int:agenda_id>", methods=["GET"])
def obtener_agenda(agenda_id):
    agenda = controller.obtener_por_id(agenda_id)
    if not agenda:
        return jsonify({"error": "no encontrada"}), 404
    return jsonify(agenda.__dict__)


@agenda_bp.route("/agenda/<int:agenda_id>", methods=["DELETE"])
def eliminar_agenda(agenda_id):
    controller.eliminar(agenda_id)
    return jsonify({"ok": True, "mensaje": "agenda eliminada"})
