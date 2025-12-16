from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from middleware.auth import login_required, role_required
from controller.consulta_c import ConsultaController
from dao.paciente_dao import PacienteDAO
from dao.receta_dao import RecetaDAO
from models.consulta import Consulta

consulta_bp = Blueprint("consulta_bp", __name__, url_prefix="/consultas")
controller = ConsultaController()

# Permitimos acceso a MEDICO y ADMIN
acceso_roles = role_required("medico", "admin")


@consulta_bp.route("/", methods=["GET"])
@login_required
@acceso_roles
def listar_consultas():
    usuario_tipo = session.get("usuario_tipo", "").lower()
    if usuario_tipo == "medico":
        id_medico = session.get("usuario_id")
        consultas = controller.listar(id_medico)
    else:  # admin ve todas las consultas
        consultas = controller.listar()
    return render_template("consultas/listar_consultas.html", consultas=consultas)


@consulta_bp.route("/crear", methods=["GET", "POST"])
@login_required
@acceso_roles
def crear_consulta():
    usuario_tipo = session.get("usuario_tipo", "").lower()

    if request.method == "POST":
        data = request.form

        # Determinar id_medico válido
        if usuario_tipo == "medico":
            id_medico = session.get("usuario_id")
            if id_medico is None:
                flash("Error: no se encontró el ID del médico en sesión", "error")
                return redirect(url_for("consulta_bp.listar_consultas"))
        else:  # admin
            id_medico_str = data.get("id_medico")
            if not id_medico_str:
                flash("Debe seleccionar un médico válido", "error")
                return redirect(url_for("consulta_bp.listar_consultas"))
            id_medico = int(id_medico_str)

        # Paciente
        id_paciente_str = data.get("id_paciente")
        if not id_paciente_str:
            flash("Debe seleccionar un paciente válido", "error")
            return redirect(url_for("consulta_bp.listar_consultas"))
        id_paciente = int(id_paciente_str)

        # Receta opcional
        id_receta = int(data["id_receta"]) if data.get("id_receta") else None

        # Crear objeto Consulta
        consulta = Consulta(
            id=None,
            id_paciente=id_paciente,
            id_medico=id_medico,
            id_receta=id_receta,
            fecha=data["fecha"],
            comentarios=data.get("comentarios", ""),
            valor=float(data.get("valor", 0))
        )

        ok = controller.crear(consulta)
        flash("Consulta creada" if ok else "Error al crear consulta")
        return redirect(url_for("consulta_bp.listar_consultas"))

    # GET: mostrar formulario
    pacientes = PacienteDAO().listar()
    recetas = RecetaDAO().listar_todas()
    return render_template("consultas/crear_consulta.html", pacientes=pacientes, recetas=recetas)


@consulta_bp.route("/editar/<int:consulta_id>", methods=["GET", "POST"])
@login_required
@acceso_roles
def editar_consulta(consulta_id):
    consulta = controller.obtener_por_id(consulta_id)
    if not consulta:
        flash("Consulta no encontrada", "error")
        return redirect(url_for("consulta_bp.listar_consultas"))

    usuario_tipo = session.get("usuario_tipo", "").lower()

    if request.method == "POST":
        data = request.form

        consulta.comentarios = data.get("comentarios", consulta.comentarios)
        consulta.fecha = data.get("fecha", consulta.fecha)
        consulta.valor = float(data.get("valor", consulta.valor))
        consulta.id_receta = int(data["id_receta"]) if data.get("id_receta") else None

        if usuario_tipo == "admin":
            id_medico_str = data.get("id_medico")
            if id_medico_str:
                consulta.id_medico = int(id_medico_str)

        ok = controller.actualizar(consulta)
        flash("Consulta actualizada" if ok else "Error al actualizar")
        return redirect(url_for("consulta_bp.listar_consultas"))

    pacientes = PacienteDAO().listar()
    recetas = RecetaDAO().listar_todas()
    return render_template("consultas/editar_consulta.html", consulta=consulta, pacientes=pacientes, recetas=recetas)


@consulta_bp.route("/eliminar/<int:consulta_id>", methods=["POST"])
@login_required
@acceso_roles
def eliminar_consulta(consulta_id):
    ok = controller.eliminar(consulta_id)
    flash("Consulta eliminada" if ok else "Error al eliminar")
    return redirect(url_for("consulta_bp.listar_consultas"))
