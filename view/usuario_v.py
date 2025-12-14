from flask import Blueprint, request, jsonify
from datetime import datetime, date
from controller.usuario_c import UsuarioController
from dao.usuario_dao import UsuarioDAO
from models.usuario import Usuario

usuario_bp = Blueprint("usuario", __name__, url_prefix="/usuarios")
usuario_controller = UsuarioController(UsuarioDAO())


def parse_fecha(fecha_str: str | None) -> date | None:
    if not fecha_str:
        return None
    try:
        return datetime.strptime(fecha_str, "%Y-%m-%d").date()
    except ValueError:
        return None


@usuario_bp.route("/crear", methods=["POST"])
def crear_usuario():
    data = request.get_json() or {}

    usuario = Usuario(
        nombre_usuario=data.get("nombre_usuario", ""),
        clave=data.get("clave", ""),
        nombre=data.get("nombre", ""),
        apellido=data.get("apellido", ""),
        fecha_nacimiento=parse_fecha(data.get("fecha_nacimiento")),
        telefono=data.get("telefono", ""),
        email=data.get("email", ""),
        tipo=data.get("tipo", "PACIENTE")
    )

    if not usuario_controller.crear(usuario):
        return jsonify({"error": "No se pudo crear usuario"}), 500

    return jsonify({"mensaje": "Usuario creado correctamente"}), 201


@usuario_bp.route("/listar", methods=["GET"])
def listar_usuarios():
    usuarios = usuario_controller.listar()
    return jsonify([u.to_dict() for u in usuarios])
