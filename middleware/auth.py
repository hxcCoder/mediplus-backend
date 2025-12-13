from functools import wraps
from flask import session, jsonify


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            return jsonify({"error": "No autenticado"}), 401
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = session.get("user")
        if not user:
            return jsonify({"error": "No autenticado"}), 401

        if user.get("tipo") != "admin":
            return jsonify({"error": "Acceso denegado: requiere rol admin"}), 403

        return f(*args, **kwargs)
    return decorated
