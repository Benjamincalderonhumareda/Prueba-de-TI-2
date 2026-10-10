# ============================================================================
# models.py — Define las tablas de la base de datos en Neon
# ============================================================================
from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB

# db es el objeto que usamos en todo el proyecto para hablar con la base de datos.
db = SQLAlchemy()


class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    edad = db.Column(db.Integer, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "edad": self.edad
        }


class LecturaPuente(db.Model):
    __tablename__ = 'lecturas_puente'

    id = db.Column(db.Integer, primary_key=True)
    nombre_puente = db.Column(db.String(100), nullable=False)
    altura_agua = db.Column(db.Float, nullable=True)
    altura_puente = db.Column(db.Float, nullable=True)
    estado_puente = db.Column(db.String(20), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=db.func.current_timestamp())

    def to_dict(self):
        return {
            "id": self.id,
            "nombre_puente": self.nombre_puente,
            "altura_agua": self.altura_agua,
            "altura_puente": self.altura_puente,
            "estado_puente": self.estado_puente,
            "fecha_registro": self.fecha_registro.strftime("%Y-%m-%d %H:%M:%S") if self.fecha_registro else None
        }


class HistorialEstadoPuente(db.Model):
    __tablename__ = 'historial_estados_puente'

    id = db.Column(db.BigInteger, primary_key=True)
    lectura_id = db.Column(db.Integer, nullable=True)
    nombre_puente = db.Column(db.String(100), nullable=False)
    estado_anterior = db.Column(db.String(20), nullable=False)
    estado_nuevo = db.Column(db.String(20), nullable=False)
    datos_anteriores = db.Column(db.JSON().with_variant(JSONB, "postgresql"), nullable=False)
    fecha_cambio = db.Column(db.DateTime(timezone=True), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "lectura_id": self.lectura_id,
            "nombre_puente": self.nombre_puente,
            "estado_anterior": self.estado_anterior,
            "estado_nuevo": self.estado_nuevo,
            "datos_anteriores": self.datos_anteriores,
            "fecha_cambio": self.fecha_cambio.isoformat() if self.fecha_cambio else None,
        }
