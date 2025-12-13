from flask import Blueprint
from controller.auth_c import AuthController

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=["POST"])
def login():
    return AuthController.login()
