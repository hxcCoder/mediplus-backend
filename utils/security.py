import bcrypt

def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

def check_password(password: str, hashed: bytes | str) -> bool:
    # Acepta hashed como bytes o str (almacenado en DB como str UTF-8)
    if isinstance(hashed, str):
        hashed = hashed.encode("utf-8")
    return bcrypt.checkpw(password.encode("utf-8"), hashed)
