from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from datetime import datetime, date
from controller.usuario_c import UsuarioController
from models.usuario import Usuario

usuario_bp = Blueprint("usuario", __name__, url_prefix="/usuarios")
usuario_controller = UsuarioController()


def parse_fecha(fecha_str: str | None) -> date | None:
    if not fecha_str:
        return None
    try:
        return datetime.strptime(fecha_str, "%Y-%m-%d").date()
    except ValueError:
        return None


# --- RUTAS API JSON ---

@usuario_bp.route("/crear", methods=["POST"])
def crear_usuario_api():
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
    if not usuario_controller.crear_usuario(usuario):
        return jsonify({"error": "No se pudo crear usuario"}), 500
    return jsonify({"mensaje": "Usuario creado correctamente"}), 201


@usuario_bp.route("/listar", methods=["GET"])
def listar_usuarios_api():
    usuarios = usuario_controller.listar_usuarios()
    return jsonify([u.to_dict() for u in usuarios])


# --- RUTAS PARA TEMPLATES HTML ---

@usuario_bp.route("/nuevo", methods=["GET", "POST"])
def crear_usuario_template():
    if request.method == "POST":
        usuario = Usuario(
            nombre_usuario=request.form.get("nombre_usuario", ""),
            clave=request.form.get("clave", ""),
            nombre=request.form.get("nombre", ""),
            apellido=request.form.get("apellido", ""),
            fecha_nacimiento=parse_fecha(request.form.get("fecha_nacimiento")),
            telefono=request.form.get("telefono", ""),
            email=request.form.get("email", ""),
            tipo=request.form.get("tipo", "PACIENTE")
        )
        if usuario_controller.crear_usuario(usuario):
            return redirect(url_for("usuario.listar_usuarios_template"))
    return render_template("usuarios/crear_usuario.html")


@usuario_bp.route("/editar/<int:usuario_id>", methods=["GET", "POST"])
def editar_usuario_template(usuario_id):
    usuario = usuario_controller.obtener_usuario(usuario_id)
    if not usuario:
        return render_template("errors/404.html"), 404
    if request.method == "POST":
        usuario.nombre_usuario = request.form.get("nombre_usuario", usuario.nombre_usuario)
        usuario.nombre = request.form.get("nombre", usuario.nombre)
        usuario.apellido = request.form.get("apellido", usuario.apellido)
        usuario.telefono = request.form.get("telefono", usuario.telefono)
        usuario.email = request.form.get("email", usuario.email)
        usuario.tipo = request.form.get("tipo", usuario.tipo)
        if usuario_controller.actualizar_usuario(usuario):
            return redirect(url_for("usuario.listar_usuarios_template"))
    return render_template("usuarios/editar_usuario.html", usuario=usuario)


@usuario_bp.route("/listar_html", methods=["GET"])
def listar_usuarios_template():
    usuarios = usuario_controller.listar_usuarios()
    return render_template("usuarios/listar_usuarios.html", usuarios=usuarios)


@usuario_bp.route("/eliminar/<int:usuario_id>", methods=["POST"])
def eliminar_usuario_template(usuario_id):
    usuario_controller.eliminar_usuario(usuario_id)
    return redirect(url_for("usuario.listar_usuarios_template"))
