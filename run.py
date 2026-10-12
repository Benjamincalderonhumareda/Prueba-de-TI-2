# ============================================================================
# run.py — Punto de entrada: aquí se arma la aplicación y se arranca
# ============================================================================
from flask import Flask, jsonify
from flask_cors import CORS  # Habilita permisos de acceso para la App Móvil/Web

from config import Config
from models import db
from routes import api_bp
from flask_swagger_ui import get_swaggerui_blueprint
from openapi import OPENAPI_SPEC

# 1. Crear la aplicación Flask
app = Flask(__name__)

# 2. Cargarle la configuración (conexión a Neon, etc.)
app.config.from_object(Config)

# 3. Habilitar CORS para permitir peticiones desde Live Server y la App
CORS(app)

# 4. Conectar SQLAlchemy (models.py) con esta app
db.init_app(app)

# 5. Registrar las rutas de la API de MayuAlert
app.register_blueprint(api_bp)

# Documentación interactiva para explorar y probar la API.
app.add_url_rule("/openapi.json", "openapi_json", lambda: jsonify(OPENAPI_SPEC))
swagger_ui = get_swaggerui_blueprint(
    "/docs", "/openapi.json", config={"app_name": "API Mayu"}
)
app.register_blueprint(swagger_ui, url_prefix="/docs")

# 6. Crear las tablas en la base de datos si no existen todavía
with app.app_context():
    db.create_all()


@app.route("/", methods=["GET"])
def inicio():
    """Ruta raíz: muestra qué endpoints existen."""
    return jsonify({
        "mensaje": "API de monitoreo de puentes MayuAlert (Flask + PostgreSQL/Neon)",
        "endpoints": {
            "GET /alertas": "Obtiene la lectura actual de cada puente",
            "GET /alertas/historial": "Obtiene transiciones de estado (fecha descendente)",
            "GET /notificaciones/clave-publica": "Devuelve la clave pública VAPID",
            "POST /notificaciones/suscripciones": "Registra o actualiza un dispositivo para Web Push",
            "DELETE /notificaciones/suscripciones": "Retira un dispositivo de Web Push",
            "GET /alertas/estado-actual": "Obtiene la última lectura del puente",
            "POST /alertas": "Registra una nueva lectura del sensor",
            "DELETE /alertas/<id>": "Elimina una lectura por su id",
            "GET /docs": "Documentación interactiva Swagger UI",
            "GET /openapi.json": "Especificación OpenAPI de la API",
        },
    })


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
