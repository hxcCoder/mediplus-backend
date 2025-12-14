from flask import Blueprint, render_template, request, redirect, url_for, flash
from middleware.auth import login_required
from controller.consulta_c import ConsultaController
from models.consulta import Consulta
from dao.paciente_dao import PacienteDAO
from dao.medico_dao import MedicoDAO
from dao.receta_dao import RecetaDAO

consulta_bp = Blueprint("consulta", __name__)
controller = ConsultaController()


@consulta_bp.route("/consultas", methods=["GET"])
@login_required
def listar_consultas():
    consultas = controller.listar()
    return render_template("consultas/listar_consultas.html", consultas=consultas)


@consulta_bp.route("/consulta/nueva", methods=["GET", "POST"])
@login_required
def crear_consulta():
    if request.method == "POST":
        data = {
            "id_paciente": request.form.get("id_paciente"),
            "id_medico": request.form.get("id_medico"),
            "id_receta": request.form.get("id_receta"),
            "fecha": request.form.get("fecha"),
            "comentarios": request.form.get("comentarios"),
            "valor": request.form.get("valor")
        }
        consulta = Consulta(**data)
        ok = controller.crear_consulta(consulta)
        flash("Consulta creada" if ok else "Error al crear consulta")
        return redirect(url_for("consulta.listar_consultas"))
    # GET -> pasar listas para selects
    pacientes = PacienteDAO().listar()
    medicos = MedicoDAO().listar()
    recetas = RecetaDAO().listar_todas()
    return render_template("consultas/crear_consulta.html", pacientes=pacientes, medicos=medicos, recetas=recetas)


@consulta_bp.route("/consulta/eliminar/<int:id_consulta>", methods=["POST"])
@login_required
def eliminar_consulta(id_consulta):
    try:
        success = controller.eliminar(id_consulta)
        flash("Consulta eliminada" if success else "Error al eliminar consulta")
    except Exception as e:
        flash(str(e))
    return redirect(url_for("consulta.listar_consultas"))


@consulta_bp.route("/consulta/editar/<int:consulta_id>", methods=["GET", "POST"])
@login_required
def editar_consulta_action(consulta_id):
    consulta = controller.obtener_por_id(consulta_id)
    if not consulta:
        flash("Consulta no encontrada")
        return redirect(url_for("consulta.listar_consultas"))

    if request.method == "POST":
        consulta.comentarios = request.form.get("comentarios", consulta.comentarios)
        consulta.fecha = request.form.get("fecha", consulta.fecha)
        consulta.valor = request.form.get("valor", consulta.valor)

        try:
            controller.actualizar_consulta(consulta)
            flash("Consulta actualizada")
        except Exception as e:
            flash(str(e))

        return redirect(url_for("consulta.listar_consultas"))

    pacientes = PacienteDAO().listar()
    medicos = MedicoDAO().listar()
    recetas = RecetaDAO().listar_todas()
    return render_template("consultas/editar_consulta.html", consulta=consulta, pacientes=pacientes, medicos=medicos, recetas=recetas)
