# app.py
from flask import Flask, request, session, jsonify
import oracledb
import bcrypt
import os
from functools import wraps
from dotenv import load_dotenv

#-- Configuracion --
load_dotenv()
app = Flask(__name__)

app.secret_key = os.getenv("FLASK_SECRET_KEY", "cambia_esta_clave")
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False  # puede cambiar a true en producción con HTTPS


#-- Conexion a oracle --
def get_connection():
    return oracledb.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        dsn=os.getenv("DB_DSN"),
        encoding="UTF-8"
    )


#-- Aqui hago el hashing --
def hash_password(plain_password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
    return hashed.decode("utf-8")

def check_password(plain_password: str, hashed: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed.encode("utf-8") if isinstance(hashed, str) else hashed
    )


# -- Middleware para seguridad --

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

#-- Registro --
@app.route('/register', methods=['POST'])
def register():
    data = request.json or {}

    username = data.get("nombre_usuario")
    password = data.get("clave")
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    tipo = data.get("tipo", "paciente").lower()

    roles_validos = ["paciente", "medico", "admin"]

    if tipo not in roles_validos:
        return jsonify({"error": "tipo de usuario inválido"}), 400

    if not username or not password or not nombre or not apellido:
        return jsonify({"error": "faltan datos obligatorios"}), 400

    hashed = hash_password(password)

    sql = """
        INSERT INTO usuario (nombre_usuario, clave, nombre, apellido, tipo)
        VALUES (:u, :c, :n, :a, :t)
    """

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(sql, [username, hashed, nombre, apellido, tipo])
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"ok": True, "mensaje": "usuario registrado"}), 201

    except oracledb.IntegrityError:
        return jsonify({"error": "nombre de usuario ya existe"}), 409
    except Exception as e:
        return jsonify({"error": "error del servidor", "detalle": str(e)}), 500

#-- Login -- 

@app.route('/login', methods=['POST'])
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

        # Guardar en sesión
        session["user"] = {
            "id": user_id,
            "nombre_usuario": nombre_usuario,
            "tipo": tipo
        }

        cur.close()
        conn.close()

        return jsonify({
            "ok": True,
            "mensaje": "inicio de sesión exitoso",
            "tipo": tipo
        }), 200

    except Exception as e:
        return jsonify({"error": "error interno", "detalle": str(e)}), 500


#-- Para deslogear --
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"ok": True, "mensaje": "sesión cerrada"}), 200


@app.route('/me', methods=['GET'])
@login_required
def me():
    user = session["user"]
    sql = """
        SELECT id, nombre_usuario, nombre, apellido, tipo
        FROM usuario
        WHERE id = :id
    """

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, [user["id"]])
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return jsonify({"error": "usuario no encontrado"}), 404

    return jsonify({
        "id": row[0],
        "nombre_usuario": row[1],
        "nombre": row[2],
        "apellido": row[3],
        "tipo": row[4]
    }), 200


#-- Panel del admin --
@app.route("/admin/panel", methods=["GET"])
@admin_required
def admin_panel():
    return jsonify({"ok": True, "mensaje": "Bienvenido al panel admin"}), 200



if __name__ == "__main__":
    app.run(debug=True)
