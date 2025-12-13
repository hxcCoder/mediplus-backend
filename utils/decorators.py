from flask import session, jsonify
from functools import wraps

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return jsonify({"error": "No autenticado"}), 401
        return f(*args, **kwargs)
    return wrapper

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user = session.get("user")
        if not user or user.get("tipo") != "admin":
            return jsonify({"error": "Acceso denegado"}), 403
        return f(*args, **kwargs)
    return wrapper
