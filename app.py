# app.py
from flask import Flask, request, session, jsonify
import oracledb
import bcrypt
import os
from functools import wraps
from dotenv import load_dotenv

# --- Configuración general ---
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "cambia_esta_clave")

# Configuración cookies sesión
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = False  # Cambiar a True en producción

# --- Conexión a ORACLE ---
def get_connection():
    return oracledb.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        dsn=os.getenv("DB_DSN"),
        encoding="UTF-8"
    )

# --- Seguridad de contraseñas ---
def hash_password(plain_password: str) -> bytes:
    if not isinstance(plain_password, str):
        raise ValueError("La contraseña debe ser un string")
    return bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())

def check_password(plain_password: str, hashed: bytes) -> bool:
    if not isinstance(plain_password, str):
        return False
    if hashed is None:
        return False
    if isinstance(hashed, str):
        hashed = hashed.encode("utf-8")
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed)

# --- Middlewares ---
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return jsonify({"error": "no autenticado"}), 401
        return f(*args, **kwargs)
    return wrapper

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user = session.get("user")
        if not user:
            return jsonify({"error": "no autenticado"}), 401
        if user.get("tipo") != "admin":
            return jsonify({"error": "acceso denegado: requiere rol admin"}), 403
        return f(*args, **kwargs)
    return wrapper

# --- Registro ---
@app.route("/register", methods=["POST"])
def register():
    data = request.json or {}

    username = data.get("nombre_usuario")
    password = data.get("clave")
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    tipo = (data.get("tipo", "paciente") or "").lower()

    ROLES = ["paciente", "medico", "admin"]

    if tipo not in ROLES:
        return jsonify({"error": "tipo inválido", "roles": ROLES}), 400

    if not all([username, password, nombre, apellido]):
        return jsonify({"error": "faltan datos"}), 400

    # Garantizar que password sea un string
    if not isinstance(password, str):
        return jsonify({"error": "contraseña inválida"}), 400

    try:
        hashed = hash_password(password)
    except Exception:
        return jsonify({"error": "contraseña inválida"}), 400

    sql = """
        INSERT INTO usuario (nombre_usuario, clave, nombre, apellido, tipo)
        VALUES (:u, :c, :n, :a, :t)
    """

    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(sql, [username, hashed, nombre, apellido, tipo])
        conn.commit()

        return jsonify({"ok": True, "mensaje": "usuario registrado"}), 201

    except oracledb.IntegrityError:
        return jsonify({"error": "usuario ya existe"}), 409

    except Exception as e:
        return jsonify({"error": "error servidor", "detalle": str(e)}), 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# --- Login ---
@app.route("/login", methods=["POST"])
def login():
    data = request.json or {}

    username = data.get("nombre_usuario")
    password = data.get("clave")

    if not username or not password:
        return jsonify({"error": "credenciales incompletas"}), 400

    sql = """
        SELECT id, nombre_usuario, clave, tipo
        FROM usuario
        WHERE nombre_usuario = :u
    """

    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(sql, [username])
        row = cur.fetchone()

        if not row:
            return jsonify({"error": "usuario no encontrado"}), 404

        user_id, nombre_usuario, hashed, tipo = row

        if not check_password(password, hashed):
            return jsonify({"error": "clave incorrecta"}), 401

        session["user"] = {
            "id": user_id,
            "nombre_usuario": nombre_usuario,
            "tipo": tipo
        }

        return jsonify({"ok": True, "mensaje": "login exitoso", "tipo": tipo}), 200

    except Exception as e:
        return jsonify({"error": "error interno", "detalle": str(e)}), 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# --- Logout ---
@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"ok": True, "mensaje": "sesión cerrada"}), 200

# --- Usuario autenticado ---
@app.route("/me", methods=["GET"])
@login_required
def me():
    sql = """
        SELECT id, nombre_usuario, nombre, apellido, tipo
        FROM usuario
        WHERE id = :id
    """

    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(sql, [session["user"]["id"]])
        row = cur.fetchone()

        if not row:
            return jsonify({"error": "usuario no encontrado"}), 404

        return jsonify({
            "id": row[0],
            "nombre_usuario": row[1],
            "nombre": row[2],
            "apellido": row[3],
            "tipo": row[4]
        }), 200

    except Exception as e:
        return jsonify({"error": "error servidor", "detalle": str(e)}), 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# --- Panel admin ---
@app.route("/admin/panel", methods=["GET"])
@admin_required
def admin_panel():
    return jsonify({"ok": True, "mensaje": "Bienvenido al panel admin"}), 200

# --- Ejecutar ---
if __name__ == "__main__":
    app.run(debug=True)
