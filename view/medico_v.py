from flask import Blueprint, request, jsonify, render_template
from datetime import datetime, date
from controller.medico_c import MedicoController
from models.medico import Medico

medico_bp = Blueprint("medico", __name__, url_prefix="/medicos")
medico_controller = MedicoController()


def parse_fecha(fecha_str: str | None) -> date | None:
    """Convierte string 'YYYY-MM-DD' a objeto date"""
    if not fecha_str:
        return None
    try:
        return datetime.strptime(fecha_str, "%Y-%m-%d").date()
    except ValueError:
        return None


@medico_bp.route("/crear", methods=["POST"])
def crear_medico():
    """Ruta para crear un médico"""
    data = request.get_json() or {}

    medico = Medico(
        nombre_usuario=data.get("nombre_usuario", ""),
        clave=data.get("clave", ""),
        nombre=data.get("nombre", ""),
        apellido=data.get("apellido", ""),
        fecha_nacimiento=parse_fecha(data.get("fecha_nacimiento")),
        telefono=data.get("telefono", ""),
        email=data.get("email", ""),
        tipo="MEDICO",
        especialidad=data.get("especialidad", ""),
        horario_atencion=data.get("horario_atencion", ""),
        fecha_ingreso=parse_fecha(data.get("fecha_ingreso"))
    )

    if not medico_controller.crear_medico(medico):
        return jsonify({"error": "No se pudo crear médico"}), 500

    return jsonify({"mensaje": "Médico creado correctamente"}), 201


@medico_bp.route("/listar", methods=["GET"])
def listar_medicos():
    """Ruta para listar todos los médicos"""
    medicos = medico_controller.listar_medicos()
    return jsonify([m.to_dict() for m in medicos])


@medico_bp.route("/editar/<int:medico_id>", methods=["PUT"])
def editar_medico(medico_id):
    """Ruta para actualizar un médico"""
    data = request.get_json() or {}
    medico = medico_controller.obtener_medico_por_id(medico_id)
    if not medico:
        return jsonify({"error": "Médico no encontrado"}), 404

    medico.nombre_usuario = data.get("nombre_usuario", medico.nombre_usuario)
    medico.nombre = data.get("nombre", medico.nombre)
    medico.apellido = data.get("apellido", medico.apellido)
    medico.telefono = data.get("telefono", medico.telefono)
    medico.email = data.get("email", medico.email)
    medico.especialidad = data.get("especialidad", medico.especialidad)
    medico.horario_atencion = data.get("horario_atencion", medico.horario_atencion)
    medico.fecha_ingreso = parse_fecha(data.get("fecha_ingreso")) or medico.fecha_ingreso

    if not medico_controller.actualizar_medico(medico):
        return jsonify({"error": "No se pudo actualizar médico"}), 500

    return jsonify({"mensaje": "Médico actualizado correctamente"}), 200


@medico_bp.route("/eliminar/<int:medico_id>", methods=["DELETE"])
def eliminar_medico(medico_id):
    """Ruta para eliminar un médico"""
    if not medico_controller.eliminar_medico(medico_id):
        return jsonify({"error": "No se pudo eliminar médico"}), 500
    return jsonify({"mensaje": "Médico eliminado correctamente"}), 200


# Opcional: rutas de renderización de templates
@medico_bp.route("/form/crear", methods=["GET"])
def form_crear_medico():
    return render_template("medico/crear_medico.html")


@medico_bp.route("/form/listar", methods=["GET"])
def form_listar_medicos():
    medicos = medico_controller.listar_medicos()
    return render_template("medico/listar_medicos.html", medicos=medicos)
