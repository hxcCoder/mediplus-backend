from functools import wraps
from flask import session, jsonify, request, redirect, url_for, flash

def login_required(f):
    """Verifica que el usuario esté autenticado."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("usuario_id"):
            if request.accept_mimetypes.accept_html:
                flash("Debes iniciar sesión")
                return redirect(url_for("login.login_form"))
            return jsonify({"error": "No autenticado"}), 401
        return f(*args, **kwargs)
    return decorated

def role_required(*roles):
    """Verifica que el usuario tenga uno de los roles permitidos."""
    roles = [r.lower() for r in roles]

    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            tipo = str(session.get("usuario_tipo", "")).lower()
            if not session.get("usuario_id"):
                if request.accept_mimetypes.accept_html:
                    flash("Debes iniciar sesión")
                    return redirect(url_for("login.login_form"))
                return jsonify({"error": "No autenticado"}), 401

            if tipo not in roles:
                if request.accept_mimetypes.accept_html:
                    flash("Acceso denegado: rol no autorizado")
                    return redirect(url_for("login.login_form"))
                return jsonify({"error": f"Acceso denegado: requiere rol {roles}"}), 403

            return f(*args, **kwargs)
        return decorated
    return decorator

admin_required = role_required("admin")
medico_required = role_required("medico")
paciente_required = role_required("paciente")
