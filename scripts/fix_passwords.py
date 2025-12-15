# fix_passwords.py
from db.connection import get_connection
from utils.security import hash_password
import bcrypt

def es_hash_bcrypt(valor: str) -> bool:
    """Verifica si un string es un hash válido de bcrypt."""
    try:
        # bcrypt siempre comienza con $2b$ o $2a$ y tiene 60 caracteres
        return (valor.startswith("$2b$") or valor.startswith("$2a$")) and len(valor) == 60
    except Exception:
        return False

def actualizar_contraseñas():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, clave FROM usuario")
    usuarios = cursor.fetchall()

    for usuario_id, clave in usuarios:
        if not es_hash_bcrypt(clave):
            nuevo_hash = hash_password(clave)
            cursor.execute(
                "UPDATE usuario SET clave = :nuevo_hash WHERE id = :usuario_id",
                nuevo_hash=nuevo_hash,
                usuario_id=usuario_id
            )
            print(f"[+] Contraseña de usuario {usuario_id} actualizada")

    conn.commit()
    cursor.close()
    conn.close()
    print("[+] Todas las contraseñas han sido revisadas y actualizadas.")

if __name__ == "__main__":
    actualizar_contraseñas()
