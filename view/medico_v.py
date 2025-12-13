# view/medico_v.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from dao.medico_dao import MedicoDAO
from models.medico import Medico

medico_bp = Blueprint("medico", __name__)
medico_dao = MedicoDAO()

# Listar médicos
@medico_bp.route("/medicos")
def listar_medicos():
    if "tipo" not in session or session["tipo"] != "admin":
        flash("Acceso denegado")
        return redirect(url_for("login.login_form"))

    medicos = medico_dao.listar()
    return render_template("medicos.html", medicos=medicos)

# Crear médico
@medico_bp.route("/medico/nuevo", methods=["GET", "POST"])
def crear_medico():
    if "tipo" not in session or session["tipo"] != "admin":
        flash("Acceso denegado")
        return redirect(url_for("login.login_form"))

    if request.method == "POST":
        medico = Medico(
            nombre_usuario=request.form["nombre_usuario"],
            clave=request.form["clave"],
            nombre=request.form["nombre"],
            apellido=request.form["apellido"],
            fecha_nacimiento=request.form["fecha_nacimiento"],
            telefono=request.form["telefono"],
            email=request.form["email"],
            especialidad=request.form["especialidad"]
        )
        medico_dao.crear(medico)
        flash("Médico creado exitosamente")
        return redirect(url_for("medico.listar_medicos"))

    return render_template("crear_medico.html")

# Editar médico
@medico_bp.route("/medico/editar/<int:medico_id>", methods=["GET", "POST"])
def editar_medico(medico_id):
    if "tipo" not in session or session["tipo"] != "admin":
        flash("Acceso denegado")
        return redirect(url_for("login.login_form"))

    medico = medico_dao.obtener_por_id(medico_id)
    if not medico:
        flash("Médico no encontrado")
        return redirect(url_for("medico.listar_medicos"))

    if request.method == "POST":
        medico.nombre_usuario = request.form["nombre_usuario"]
        medico.nombre = request.form["nombre"]
        medico.apellido = request.form["apellido"]
        medico.fecha_nacimiento = request.form["fecha_nacimiento"]
        medico.telefono = request.form["telefono"]
        medico.email = request.form["email"]
        medico.especialidad = request.form["especialidad"]
        medico_dao.actualizar(medico)
        flash("Médico actualizado")
        return redirect(url_for("medico.listar_medicos"))

    return render_template("editar_medico.html", medico=medico)

# Eliminar médico
@medico_bp.route("/medico/eliminar/<int:medico_id>")
def eliminar_medico(medico_id):
    if "tipo" not in session or session["tipo"] != "admin":
        flash("Acceso denegado")
        return redirect(url_for("login.login_form"))

    medico_dao.eliminar(medico_id)
    flash("Médico eliminado")
    return redirect(url_for("medico.listar_medicos"))
