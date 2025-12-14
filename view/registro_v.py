from flask import Blueprint, render_template, request, redirect, url_for, flash
from dao.usuario_dao import UsuarioDAO
from controller.usuario_c import UsuarioController
from models.usuario import Usuario
from datetime import datetime

registro_bp = Blueprint("registro", __name__)
usuario_dao = UsuarioDAO()
usuario_controller = UsuarioController(usuario_dao)


@registro_bp.route("/register", methods=["GET"])
def register_form():
    return render_template("auth/register.html")


@registro_bp.route("/register", methods=["POST"])
def register_action():
    nombre_usuario = request.form.get("nombre_usuario")
    clave = request.form.get("clave")
    nombre = request.form.get("nombre") or ""
    apellido = request.form.get("apellido") or ""
    fecha_nacimiento = request.form.get("fecha_nacimiento")
    telefono = request.form.get("telefono") or ""
    email = request.form.get("email") or ""
    tipo = request.form.get("tipo")

    if not nombre_usuario or not clave or not tipo:
        flash("Debes completar los campos obligatorios")
        return redirect(url_for("registro.register_form"))

    nuevo_usuario = Usuario(
        nombre_usuario=nombre_usuario,
        clave=clave,
        nombre=nombre,
        apellido=apellido,
        fecha_nacimiento=datetime.strptime(fecha_nacimiento, "%Y-%m-%d").date() if fecha_nacimiento else None,
        telefono=telefono,
        email=email,
        tipo=tipo
    )

    exito = usuario_controller.crear(nuevo_usuario)
    flash("Usuario registrado correctamente" if exito else "Error al registrar usuario")
    return redirect(url_for("login.login_form") if exito else url_for("registro.register_form"))
