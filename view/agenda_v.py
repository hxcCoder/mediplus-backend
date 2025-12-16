from flask import Blueprint, render_template, session
from middleware.auth import login_required, medico_required
from dao.agenda_dao import AgendaDAO

agenda_bp = Blueprint("agenda_bp", __name__, url_prefix="/agenda")
agenda_dao = AgendaDAO()

@agenda_bp.route("/", methods=["GET"])
@login_required
@medico_required
def listar_agenda():
    id_medico = session["usuario_id"]
    agendas = [a for a in agenda_dao.listar() if a.id_medico == id_medico]
    return render_template("agenda/listar_agenda.html", agendas=agendas)
