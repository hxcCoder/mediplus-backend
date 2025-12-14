from functools import wraps
from flask import session, jsonify, request, redirect, url_for, flash


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Acepta dos estilos: sesión con clave 'user' (dict) o claves separadas 'user_id'/'tipo'
        if "user" not in session and "user_id" not in session:
            # Si la petición acepta HTML, redirigimos al login con flash
            if request.accept_mimetypes.accept_html:
                flash("Debes iniciar sesión")
                return redirect(url_for("login.login_form"))
            return jsonify({"error": "No autenticado"}), 401
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = session.get("user")
        tipo = None
        if user and isinstance(user, dict):
            tipo = user.get("tipo")
        else:
            tipo = session.get("tipo")

        if not tipo:
            if request.accept_mimetypes.accept_html:
                flash("Debes iniciar sesión")
                return redirect(url_for("login.login_form"))
            return jsonify({"error": "No autenticado"}), 401

        if str(tipo).lower() != "admin":
            if request.accept_mimetypes.accept_html:
                flash("Acceso denegado: requiere rol admin")
                return redirect(url_for("login.login_form"))
            return jsonify({"error": "Acceso denegado: requiere rol admin"}), 403

        return f(*args, **kwargs)
    return decorated
