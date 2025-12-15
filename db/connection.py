import os
import oracledb
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    conn = oracledb.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        dsn=os.getenv("DB_DSN")
    )
    with conn.cursor() as cursor:
        cursor.execute("ALTER SESSION SET CURRENT_SCHEMA = APP_USER")
    return conn
