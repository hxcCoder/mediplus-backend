from flask import Blueprint, request, jsonify, session, render_template, flash, redirect, url_for
from datetime import datetime, date
from middleware.auth import admin_required
from controller.usuario_c import UsuarioController
from dao.usuario_dao import UsuarioDAO
from models.usuario import Usuario

# Inicializar DAO y Controller
usuario_dao = UsuarioDAO()
usuario_controller = UsuarioController(usuario_dao)

usuario_bp = Blueprint("usuario", __name__, url_prefix="/usuarios")


def parse_fecha(fecha_str: str | None) -> date | None:
    """Convierte string YYYY-MM-DD a date, retorna None si es inválido."""
    if fecha_str:
        try:
            return datetime.strptime(fecha_str, "%Y-%m-%d").date()
        except ValueError:
            return None
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

    ok = usuario_controller.crear_usuario(usuario)
    if not ok:
        return jsonify({"error": "No se pudo crear el usuario"}), 500

    return jsonify({"mensaje": "Usuario creado correctamente"}), 201


@usuario_bp.route("/<int:usuario_id>", methods=["GET"])
def obtener_usuario(usuario_id: int):
    usuario = usuario_controller.obtener_usuario(usuario_id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify({
        "id": usuario.id,
        "nombre_usuario": usuario.nombre_usuario,
        "nombre": usuario.nombre,
        "apellido": usuario.apellido,
        "fecha_nacimiento": usuario.fecha_nacimiento.isoformat() if usuario.fecha_nacimiento else None,
        "telefono": usuario.telefono,
        "email": usuario.email,
        "tipo": usuario.tipo
    })


@usuario_bp.route("/actualizar/<int:usuario_id>", methods=["PUT"])
def actualizar_usuario(usuario_id: int):
    data = request.get_json() or {}

    usuario_existente = usuario_controller.obtener_usuario(usuario_id)
    if not usuario_existente:
        return jsonify({"error": "Usuario no encontrado"}), 404

    # Actualizamos solo los campos que existen
    usuario_existente.nombre_usuario = data.get("nombre_usuario", usuario_existente.nombre_usuario)
    usuario_existente.nombre = data.get("nombre", usuario_existente.nombre)
    usuario_existente.apellido = data.get("apellido", usuario_existente.apellido)
    usuario_existente.fecha_nacimiento = parse_fecha(data.get("fecha_nacimiento")) or usuario_existente.fecha_nacimiento
    usuario_existente.telefono = data.get("telefono", usuario_existente.telefono)
    usuario_existente.email = data.get("email", usuario_existente.email)
    usuario_existente.tipo = data.get("tipo", usuario_existente.tipo)

    ok = usuario_controller.actualizar_usuario(usuario_existente)
    if not ok:
        return jsonify({"error": "No se pudo actualizar el usuario"}), 500

    return jsonify({"mensaje": "Usuario actualizado correctamente"}), 200


@usuario_bp.route("/editar", methods=["GET", "POST"])
def editar_usuario():
    # Editar perfil propio
    user = None
    if "user" in session:
        user = session["user"]
    elif "user_id" in session:
        user = {"id": session.get("user_id")}

    if not user:
        return jsonify({"error": "No autenticado"}), 401

    usuario = usuario_controller.obtener_usuario(user.get("id"))
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    if request.method == "POST":
        data = request.get_json() or {}
        usuario.nombre = data.get("nombre", usuario.nombre)
        usuario.apellido = data.get("apellido", usuario.apellido)
        usuario.telefono = data.get("telefono", usuario.telefono)
        usuario.email = data.get("email", usuario.email)

        ok = usuario_controller.actualizar_usuario(usuario)
        if not ok:
            return jsonify({"error": "No se pudo actualizar"}), 500
        flash("Perfil actualizado correctamente")
        return jsonify({"mensaje": "Perfil actualizado"}), 200

    # GET -> devolver datos para llenar el formulario
    if request.accept_mimetypes.accept_html:
        return render_template("usuario/editar_usuario.html", usuario=usuario)

    return jsonify({
        "id": usuario.id,
        "nombre_usuario": usuario.nombre_usuario,
        "nombre": usuario.nombre,
        "apellido": usuario.apellido,
        "fecha_nacimiento": usuario.fecha_nacimiento.isoformat() if usuario.fecha_nacimiento else None,
        "telefono": usuario.telefono,
        "email": usuario.email,
        "tipo": usuario.tipo
    })


@usuario_bp.route("/listar")
@admin_required
def listar_usuarios():
    usuarios = usuario_controller.listar()
    try:
        return render_template("usuario/listar_usuarios.html", usuarios=usuarios)
    except Exception:
        # Fallback JSON para APIs
        return jsonify([{
            "id": u.id,
            "nombre_usuario": u.nombre_usuario,
            "nombre": u.nombre,
            "apellido": u.apellido,
            "email": u.email,
            "tipo": u.tipo
        } for u in usuarios])
