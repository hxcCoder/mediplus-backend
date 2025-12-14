from flask import Blueprint, render_template, request, redirect, url_for, flash
from middleware.auth import admin_required
from dao.paciente_dao import PacienteDAO
from models.paciente import Paciente
from datetime import datetime

paciente_bp = Blueprint("paciente", __name__, url_prefix="/paciente")
paciente_dao = PacienteDAO()


# ------------------------------
# Listar pacientes
# ------------------------------
@paciente_bp.route("/listar")
@admin_required
def listar_pacientes():
    pacientes = paciente_dao.listar()
    return render_template("paciente/listar_pacientes.html", pacientes=pacientes)


# ------------------------------
# Crear paciente
# ------------------------------
@paciente_bp.route("/crear", methods=["GET", "POST"])
@admin_required
def crear_paciente():
    if request.method == "POST":
        _f1 = request.form.get("fecha_primera_visita")
        paciente = Paciente(
            nombre_usuario=request.form["nombre_usuario"],
            clave=request.form["clave"],
            nombre=request.form["nombre"],
            apellido=request.form["apellido"],
            fecha_nacimiento=datetime.strptime(request.form["fecha_nacimiento"], "%Y-%m-%d").date() if request.form.get("fecha_nacimiento") else None,
            telefono=request.form["telefono"],
            email=request.form["email"],
            comuna=request.form.get("comuna"),
            fecha_primera_visita=datetime.strptime(_f1, "%Y-%m-%d").date() if _f1 else None
        )

        paciente_dao.crear(paciente)
        flash("Paciente creado correctamente")
        return redirect(url_for("paciente.listar_pacientes"))

    return render_template("paciente/crear_paciente.html")


# ------------------------------
# Editar paciente
# ------------------------------
@paciente_bp.route("/editar/<int:paciente_id>", methods=["GET", "POST"])
@admin_required
def editar_paciente(paciente_id):
    paciente = paciente_dao.obtener_por_id(paciente_id)
    if not paciente:
        flash("Paciente no encontrado")
        return redirect(url_for("paciente.listar_pacientes"))

    if request.method == "POST":
        paciente.nombre_usuario = request.form["nombre_usuario"]
        paciente.nombre = request.form["nombre"]
        paciente.apellido = request.form["apellido"]
        paciente.fecha_nacimiento = datetime.strptime(request.form["fecha_nacimiento"], "%Y-%m-%d").date() if request.form.get("fecha_nacimiento") else paciente.fecha_nacimiento
        paciente.telefono = request.form["telefono"]
        paciente.email = request.form["email"]
        paciente.comuna = request.form.get("comuna")
        _f1 = request.form.get("fecha_primera_visita")
        paciente.fecha_primera_visita = datetime.strptime(_f1, "%Y-%m-%d").date() if _f1 else paciente.fecha_primera_visita

        paciente_dao.actualizar(paciente)
        flash("Paciente actualizado correctamente")
        return redirect(url_for("paciente.listar_pacientes"))

    return render_template("paciente/editar_paciente.html", paciente=paciente)


# ------------------------------
# Eliminar paciente
# ------------------------------
@paciente_bp.route("/eliminar/<int:paciente_id>", methods=["GET","POST"])
@admin_required
def eliminar_paciente(paciente_id):
    paciente = paciente_dao.obtener_por_id(paciente_id)
    if not paciente:
        flash("Paciente no encontrado")
        return redirect(url_for("paciente.listar_pacientes"))

    if request.method == "POST":
        paciente_dao.eliminar(paciente_id)
        flash("Paciente eliminado correctamente")
        return redirect(url_for("paciente.listar_pacientes"))

    return render_template("paciente/eliminar_paciente.html", paciente=paciente)
