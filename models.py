# ============================================================================
# models.py — Define cómo se ve la tabla "usuarios" en la base de datos
# ============================================================================
from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

# db es el objeto que usamos en todo el proyecto para hablar con la
# base de datos. Se conecta a la app de Flask en run.py.
db = SQLAlchemy()


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
