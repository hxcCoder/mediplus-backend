from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from middleware.auth import login_required, medico_required
from controller.consulta_c import ConsultaController
from dao.paciente_dao import PacienteDAO
from dao.receta_dao import RecetaDAO
from models.consulta import Consulta

consulta_bp = Blueprint("consulta_bp", __name__, url_prefix="/consultas")
controller = ConsultaController()

@consulta_bp.route("/", methods=["GET"])
@login_required
@medico_required
def listar_consultas():
    id_medico = session["usuario_id"]
    consultas = controller.listar(id_medico)
    return render_template("consultas/listar_consultas.html", consultas=consultas)

@consulta_bp.route("/crear", methods=["GET", "POST"])
@login_required
@medico_required
def crear_consulta():
    if request.method == "POST":
        data = request.form
        consulta = Consulta(
            id=None,
            id_paciente=int(data["id_paciente"]),
            id_medico=session["usuario_id"],
            id_receta=int(data["id_receta"]) if data.get("id_receta") else None,
            fecha=data["fecha"],
            comentarios=data.get("comentarios", ""),
            valor=float(data.get("valor", 0))
        )
        ok = controller.crear(consulta)
        flash("Consulta creada" if ok else "Error al crear consulta")
        return redirect(url_for("consulta_bp.listar_consultas"))

    pacientes = PacienteDAO().listar()
    recetas = RecetaDAO().listar_todas()
    return render_template("consultas/crear_consulta.html", pacientes=pacientes, recetas=recetas)

@consulta_bp.route("/editar/<int:consulta_id>", methods=["GET", "POST"])
@login_required
@medico_required
def editar_consulta(consulta_id):
    consulta = controller.obtener_por_id(consulta_id)
    if not consulta:
        flash("Consulta no encontrada", "error")
        return redirect(url_for("consulta_bp.listar_consultas"))

    if request.method == "POST":
        data = request.form
        consulta.comentarios = data.get("comentarios", consulta.comentarios)
        consulta.fecha = data.get("fecha", consulta.fecha)
        consulta.valor = float(data.get("valor", consulta.valor))
        consulta.id_receta = int(data["id_receta"]) if data.get("id_receta") else None
        ok = controller.actualizar(consulta)
        flash("Consulta actualizada" if ok else "Error al actualizar")
        return redirect(url_for("consulta_bp.listar_consultas"))

    pacientes = PacienteDAO().listar()
    recetas = RecetaDAO().listar_todas()
    return render_template("consultas/editar_consulta.html", consulta=consulta, pacientes=pacientes, recetas=recetas)

@consulta_bp.route("/eliminar/<int:consulta_id>", methods=["POST"])
@login_required
@medico_required
def eliminar_consulta(consulta_id):
    ok = controller.eliminar(consulta_id)
    flash("Consulta eliminada" if ok else "Error al eliminar")
    return redirect(url_for("consulta_bp.listar_consultas"))
