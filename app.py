# app.py
from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "cambiar")

# Cookies
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = False

# Blueprints
from view.login_v import login_bp
from view.registro_v import registro_bp
from view.auth_v import auth_bp
from view.agenda_v import agenda_bp

app.register_blueprint(login_bp)
app.register_blueprint(registro_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(agenda_bp)

if __name__ == "__main__":
    app.run(debug=True)
