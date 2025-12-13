from flask import Blueprint, jsonify
from controller.usuario_c import UsuarioController
from dao.usuario_dao import UsuarioDAO

usuario_dao = UsuarioDAO()
usuario_controller = UsuarioController(usuario_dao)

usuario_bp = Blueprint("usuario", __name__, url_prefix="/usuarios")


@usuario_bp.route("/", methods=["GET"])
def listar_usuarios():
    usuarios = usuario_controller.listar()
    return jsonify([u.to_dict() for u in usuarios]), 200


@usuario_bp.route("/<int:user_id>", methods=["GET"])
def obtener_usuario(user_id):
    usuario = usuario_controller.obtener_por_id(user_id)
    if not usuario:
        return jsonify({"error": "usuario no encontrado"}), 404
    return jsonify(usuario.to_dict()), 200
