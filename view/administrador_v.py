from flask import Blueprint, render_template, request, redirect, url_for, flash
from middleware.auth import admin_required
from dao.administrador_dao import AdministradorDAO
from models.administrador import Administrador
from datetime import datetime

admin_bp = Blueprint("administrador", __name__, url_prefix="/administrador")
admin_dao = AdministradorDAO()


# Listar administradores

@admin_bp.route("/listar")
@admin_required
def listar_administradores():
    admins = admin_dao.listar()
    return render_template("administrador/listar_admin.html", administradores=admins)


# Crear administrador
@admin_bp.route("/crear", methods=["GET", "POST"])
@admin_required
def crear_administrador():
    if request.method == "POST":
        admin = Administrador(
            nombre_usuario=request.form["nombre_usuario"],
            clave=request.form["clave"],
            nombre=request.form["nombre"],
            apellido=request.form["apellido"],
            fecha_nacimiento=datetime.strptime(request.form["fecha_nacimiento"], "%Y-%m-%d").date() 
                            if request.form.get("fecha_nacimiento") else None,
            telefono=request.form["telefono"],
            email=request.form["email"]
        )

        exito = admin_dao.crear(admin)
        flash("Administrador creado correctamente" if exito else "Error al crear administrador")
        return redirect(url_for("administrador.listar_administradores"))

    return render_template("administrador/crear_admin.html")


# Editar administrador
@admin_bp.route("/editar/<int:admin_id>", methods=["GET", "POST"])
@admin_required
def editar_administrador(admin_id):
    admin = admin_dao.obtener_por_id(admin_id)
    if not admin:
        flash("Administrador no encontrado")
        return redirect(url_for("administrador.listar_administradores"))

    if request.method == "POST":
        admin.nombre_usuario = request.form["nombre_usuario"]
        admin.nombre = request.form["nombre"]
        admin.apellido = request.form["apellido"]
        admin.fecha_nacimiento = datetime.strptime(request.form["fecha_nacimiento"], "%Y-%m-%d").date() \
                                if request.form.get("fecha_nacimiento") else admin.fecha_nacimiento
        admin.telefono = request.form["telefono"]
        admin.email = request.form["email"]

        exito = admin_dao.actualizar(admin)
        flash("Administrador actualizado correctamente" if exito else "Error al actualizar administrador")
        return redirect(url_for("administrador.listar_administradores"))

    return render_template("administrador/editar_admin.html", administrador=admin)


# Eliminar administrador
@admin_bp.route("/eliminar/<int:admin_id>")
@admin_required
def eliminar_administrador(admin_id):
    exito = admin_dao.eliminar(admin_id)
    flash("Administrador eliminado correctamente" if exito else "Error al eliminar administrador")
    return redirect(url_for("administrador.listar_administradores"))
