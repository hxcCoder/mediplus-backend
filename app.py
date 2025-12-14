from flask import Flask, render_template
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "cambiar_por_entorno")

    # Config según entorno
    app.config["DEBUG"] = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = os.getenv("SESSION_COOKIE_SAMESITE", "Lax")
    # En producción debe ser True; en desarrollo se puede usar False
    app.config["SESSION_COOKIE_SECURE"] = os.getenv("SESSION_COOKIE_SECURE", "false").lower() == "true"

    # Blueprints: registrar todos los que implemente el proyecto
    from view.login_v import login_bp
    from view.registro_v import registro_bp
    from view.auth_v import auth_bp
    from view.agenda_v import agenda_bp
    from view.medico_v import medico_bp
    from view.paciente_v import paciente_bp
    from view.administrador_v import admin_bp
    from view.insumo_v import insumo_bp
    from view.receta_v import receta_bp
    from view.usuario_v import usuario_bp
    from view.menu_admin_v import menu_admin_bp
    from view.menu_medico_v import menu_medico_bp
    from view.menu_paciente_v import menu_paciente_bp

    app.register_blueprint(login_bp)
    app.register_blueprint(registro_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(agenda_bp)
    app.register_blueprint(medico_bp)
    app.register_blueprint(paciente_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(insumo_bp)
    app.register_blueprint(receta_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(menu_admin_bp)
    app.register_blueprint(menu_medico_bp)
    app.register_blueprint(menu_paciente_bp)
    
    # Handlers básicos
    @app.errorhandler(404)
    def not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template("errors/500.html"), 500

    # Filtros de Jinja
    def format_clp(value: int | float | None) -> str:
        if value is None:
            return "-"
        try:
            v = int(value)
        except Exception:
            try:
                v = round(float(value))
            except Exception:
                return str(value)
        return f"${v:,}".replace(",", ".") + " CLP"

    app.add_template_filter(format_clp, name="format_clp")

    return app

if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))