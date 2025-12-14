from flask import Blueprint, request, jsonify
from datetime import datetime
from controller.auth_c import AuthController
from dao.usuario_dao import UsuarioDAO
from models.usuario import Usuario

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

usuario_dao = UsuarioDAO()
auth_controller = AuthController(usuario_dao)


def parse_fecha(fecha_str):
    if fecha_str:
        try:
            return datetime.strptime(fecha_str, "%Y-%m-%d").date()
        except ValueError:
            return None
    return None


@auth_bp.route("/register", methods=["POST"])
def register():
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

    ok = auth_controller.registrar_usuario(usuario)

    if not ok:
        return jsonify({"error": "No se pudo registrar el usuario"}), 400

    return jsonify({"mensaje": "Usuario registrado correctamente"}), 201
