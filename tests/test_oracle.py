from db.connection import get_connection

conn = get_connection()
print("✅ Conectado a Oracle")
conn.close()
