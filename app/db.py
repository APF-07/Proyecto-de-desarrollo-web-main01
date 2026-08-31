import os
from google.cloud.sql.connector import Connector
import sqlalchemy
from app.config import Config

# 1. Inicializar el conector de Google Cloud SQL
connector = Connector()

def getconn():
    """Función de conexión nativa mediante Cloud SQL Connector y pytds"""
    # Se obtienen las variables de entorno o valores de Config
    instance_connection_name = os.environ.get(
        "INSTANCE_CONNECTION_NAME", 
        getattr(Config, "INSTANCE_CONNECTION_NAME", "")
    )
    db_user = os.environ.get("DB_USER", getattr(Config, "DB_USER", "sqlserver"))
    db_password = os.environ.get("DB_PASSWORD", getattr(Config, "DB_PASSWORD", ""))
    db_name = os.environ.get("DB_NAME", getattr(Config, "DB_NAME", "INVENTARIO"))

    conn = connector.connect(
        instance_connection_name,
        "pytds",
        user=db_user,
        password=db_password,
        db=db_name
    )
    return conn

# 2. Si tus modelos esperan un objeto tipo conexión cruda (cursor / commit)
def get_connection():
    try:
        # En la nube (App Engine) usa el conector de Cloud SQL
        if os.environ.get("INSTANCE_CONNECTION_NAME"):
            return getconn()
        else:
            # Si estás en tu computadora local ejecutando con Windows
            import pyodbc
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