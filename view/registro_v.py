# view/registro_v.py
from flask import Blueprint, render_template, request, jsonify
from controller.auth_c import AuthController

registro_bp = Blueprint("registro", __name__)

# --- Vista GET del formulario ---
@registro_bp.route("/register", methods=["GET"])
def register_form():
    return render_template("register.html")  # Debes crear templates/register.html


# --- Enviar datos al controlador ---
@registro_bp.route("/register", methods=["POST"])
def register_action():
    return AuthController.register()
