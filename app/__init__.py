from flask import Flask
from flask_login import LoginManager
from app.config import Config
from app.db import get_connection

# Inicializar LoginManager
login_manager = LoginManager()
login_manager.login_view = 'main.login' # A dónde ir si no estás logueado
login_manager.login_message = "Por favor inicia sesión para acceder."
login_manager.login_message_category = "warning"

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    login_manager.init_app(app)

    # Función para cargar usuario
    from app.models import obtener_usuario_por_id
    @login_manager.user_loader
    def load_user(user_id):
        return obtener_usuario_por_id(int(user_id))

    # Conexión test al iniciar
    @app.before_request
    def before_request():
        conn = get_connection()
        if conn:
            conn.close()

    # Registrar rutas
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app