# ============================================================================
# config.py — Configuración de la aplicación y conexión a la base de datos
# ============================================================================
import os
from dotenv import load_dotenv

# Carga las variables definidas en el archivo .env
load_dotenv()


def obtener_database_uri():
    """
    Lee la cadena de conexión desde la variable de entorno DATABASE_URL.
    Si no existe, usa SQLite local para facilitar el desarrollo sin
    depender de un servicio externo como Neon.
    """
    database_url = os.environ.get("DATABASE_URL") or "sqlite:///local.db"

    # SQLAlchemy necesita el driver "psycopg" explícito en la URL
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql+psycopg://", 1)
    elif database_url.startswith("postgresql://"):
        database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)

    return database_url


class Config:
    """Agrupa toda la configuración de Flask en un solo lugar."""
    SQLALCHEMY_DATABASE_URI = obtener_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False