import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "clave_segura_agricola")
    # Usamos r"" para que la barra invertida \ se lea correctamente
    DB_SERVER = os.environ.get("DB_SERVER", r"A-FIRE\SQLEXPRESS")
    DB_NAME = os.environ.get("DB_NAME", "INVENTARIO")
    # Al usar autenticación de Windows, estos campos no son necesarios
    DB_USER = os.environ.get("DB_USER", "")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "")