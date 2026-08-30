# ============================================================================
# models.py — Define las tablas de la base de datos en Neon
# ============================================================================
from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

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
    nivel_caudal = db.Column(db.Float, nullable=False)
    estado_puente = db.Column(db.String(20), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=db.func.current_timestamp())

    def to_dict(self):
        return {
            "id": self.id,
            "nombre_puente": self.nombre_puente,
            "nivel_caudal": self.nivel_caudal,
            "estado_puente": self.estado_puente,
            "fecha_registro": self.fecha_registro.strftime("%Y-%m-%d %H:%M:%S") if self.fecha_registro else None
        }
