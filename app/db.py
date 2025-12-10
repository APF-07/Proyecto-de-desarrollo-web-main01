import pyodbc
from app.config import Config

def get_connection():
    try:
        # Se elimina UID/PWD y se agrega Trusted_Connection=yes
        conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={Config.DB_SERVER};"
            f"DATABASE={Config.DB_NAME};"
            f"Trusted_Connection=yes;"
        )
        return conn
    except Exception as e:
        print("❌ Error de conexión:", e)
        return None