import os
import oracledb
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    conn = oracledb.connect(
        user=os.getenv("DB_USER"),       # debe ser APP_USER
        password=os.getenv("DB_PASS"),
        dsn=os.getenv("DB_DSN")
    )

    cursor = conn.cursor()
    cursor.execute("ALTER SESSION SET CURRENT_SCHEMA = APP_USER")  # Cambia SYSTEM por APP_USER
    cursor.close()

    return conn
