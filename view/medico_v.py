from flask import Blueprint, render_template, request, redirect, url_for, flash
from middleware.auth import admin_required
from dao.medico_dao import MedicoDAO
from models.medico import Medico
from datetime import datetime

medico_bp = Blueprint("medico", __name__, url_prefix="/medico")
medico_dao = MedicoDAO()


# ------------------------------
# Listar médicos
# ------------------------------
@medico_bp.route("/listar")
@admin_required
def listar_medicos():
    medicos = medico_dao.listar()
    return render_template("medico/listar_medicos.html", medicos=medicos)


# ------------------------------
# Crear médico
# ------------------------------
@medico_bp.route("/crear", methods=["GET", "POST"])
@admin_required
def crear_medico():
    if request.method == "POST":

        medico = Medico(
            nombre_usuario=request.form["nombre_usuario"],
            clave=request.form["clave"],
            nombre=request.form["nombre"],
            apellido=request.form["apellido"],
            fecha_nacimiento=datetime.strptime(request.form["fecha_nacimiento"], "%Y-%m-%d").date() if request.form.get("fecha_nacimiento") else None,
            telefono=request.form["telefono"],
            email=request.form["email"],
            especialidad=request.form["especialidad"]
        )

        medico_dao.crear(medico)
        flash("Médico creado correctamente")
        return redirect(url_for("medico.listar_medicos"))

    return render_template("medico/crear_medico.html")


# ------------------------------
# Editar médico
# ------------------------------
@medico_bp.route("/editar/<int:medico_id>", methods=["GET", "POST"])
@admin_required
def editar_medico(medico_id):
    medico = medico_dao.obtener_por_id(medico_id)
    if not medico:
        flash("Médico no encontrado")
        return redirect(url_for("medico.listar_medicos"))

    if request.method == "POST":
        medico.nombre_usuario = request.form["nombre_usuario"]
        medico.nombre = request.form["nombre"]
        medico.apellido = request.form["apellido"]
        medico.fecha_nacimiento = datetime.strptime(request.form["fecha_nacimiento"], "%Y-%m-%d").date() if request.form.get("fecha_nacimiento") else medico.fecha_nacimiento
        medico.telefono = request.form["telefono"]
        medico.email = request.form["email"]
        medico.especialidad = request.form["especialidad"]

        medico_dao.actualizar(medico)
        flash("Médico actualizado correctamente")
        return redirect(url_for("medico.listar_medicos"))

    return render_template("medico/editar_medico.html", medico=medico)


# ------------------------------
# Eliminar médico
# ------------------------------
@medico_bp.route("/eliminar/<int:medico_id>", methods=["GET","POST"])
@admin_required
def eliminar_medico(medico_id):
    medico = medico_dao.obtener_por_id(medico_id)
    if not medico:
        flash("Médico no encontrado")
        return redirect(url_for("medico.listar_medicos"))

    if request.method == "POST":
        medico_dao.eliminar(medico_id)
        flash("Médico eliminado correctamente")
        return redirect(url_for("medico.listar_medicos"))

    return render_template("medico/eliminar_medico.html", medico=medico)
