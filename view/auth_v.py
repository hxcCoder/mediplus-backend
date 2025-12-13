from flask import Blueprint, request, jsonify, session
from controller.auth_c import AuthController
from models.usuario import Usuario

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
auth_controller = AuthController()


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Datos no enviados"}), 400

    nombre_usuario = data.get("nombre_usuario")
    clave = data.get("clave")

    if not nombre_usuario or not clave:
        return jsonify({"error": "Usuario y contraseña son obligatorios"}), 400

    usuario = auth_controller.login(nombre_usuario, clave)

    if not usuario:
        return jsonify({"error": "Credenciales inválidas"}), 401

    # Manejo de sesión
    session["usuario_id"] = usuario.id
    session["tipo"] = usuario.tipo
    session["nombre_usuario"] = usuario.nombre_usuario

    return jsonify({
        "mensaje": "Login exitoso",
        "usuario": {
            "id": usuario.id,
            "nombre_usuario": usuario.nombre_usuario,
            "tipo": usuario.tipo
        }
    }), 200


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"mensaje": "Sesión cerrada correctamente"}), 200


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Datos no enviados"}), 400

    try:
        usuario = Usuario(
            nombre_usuario=data.get("nombre_usuario"),
            clave=data.get("clave"),
            nombre=data.get("nombre"),
            apellido=data.get("apellido"),
            fecha_nacimiento=data.get("fecha_nacimiento"),
            telefono=data.get("telefono"),
            email=data.get("email"),
            tipo=data.get("tipo", "PACIENTE")
        )

        ok = auth_controller.registrar_usuario(usuario)

        if not ok:
            return jsonify({"error": "No se pudo registrar el usuario"}), 500

        return jsonify({"mensaje": "Usuario registrado correctamente"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400
