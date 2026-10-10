# ============================================================================
# routes.py — Los endpoints de la API: qué pasa cuando llega cada petición
# ============================================================================
from flask import Blueprint, request, jsonify
from models import db, Usuario, LecturaPuente, HistorialEstadoPuente

# Un Blueprint agrupa un conjunto de rutas relacionadas para luego "engancharlas" a la app principal en run.py.
usuarios_bp = Blueprint("usuarios", __name__)


@usuarios_bp.route("/usuarios", methods=["GET"])
def listar_usuarios():
    """GET /usuarios → devuelve todos los usuarios."""
    usuarios = Usuario.query.all()
    return jsonify([u.to_dict() for u in usuarios])


@usuarios_bp.route("/usuarios/<int:usuario_id>", methods=["GET"])
def buscar_usuario(usuario_id):
    """GET /usuarios/5 → busca y devuelve un solo usuario por id."""
    usuario = db.session.get(Usuario, usuario_id)
    if usuario is None:
        return jsonify({"error": "Usuario no encontrado."}), 404
    return jsonify(usuario.to_dict())


@usuarios_bp.route("/usuarios", methods=["POST"])
def agregar_usuario():
    """POST /usuarios → agrega un usuario nuevo."""
    datos = request.get_json()

    nuevo_usuario = Usuario(
        nombre=datos["nombre"],
        email=datos["email"],
        edad=datos.get("edad"),
    )

    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify(nuevo_usuario.to_dict()), 201


@usuarios_bp.route("/usuarios/<int:usuario_id>", methods=["PUT"])
def editar_usuario(usuario_id):
    """PUT /usuarios/5 → edita los datos de un usuario existente."""
    usuario = db.session.get(Usuario, usuario_id)
    if usuario is None:
        return jsonify({"error": "Usuario no encontrado."}), 404

    datos = request.get_json()

    usuario.nombre = datos.get("nombre", usuario.nombre)
    usuario.email = datos.get("email", usuario.email)
    usuario.edad = datos.get("edad", usuario.edad)

    db.session.commit()

    return jsonify(usuario.to_dict())


@usuarios_bp.route("/usuarios/<int:usuario_id>", methods=["DELETE"])
def eliminar_usuario(usuario_id):
    """DELETE /usuarios/5 → elimina un usuario."""
    usuario = db.session.get(Usuario, usuario_id)
    if usuario is None:
        return jsonify({"error": "Usuario no encontrado."}), 404

    db.session.delete(usuario)
    db.session.commit()

    return jsonify({"mensaje": "Usuario eliminado correctamente."})


# ============================================================================
# ENDPOINTS PARA EL SISTEMA DE ALERTA TEMPRANA DE HUAYCO (ARDUINO/PUENTE)
# ============================================================================

@usuarios_bp.route("/alertas", methods=["GET"])
def listar_alertas():
    """Devuelve la lectura actual de cada puente."""
    lecturas = LecturaPuente.query.order_by(LecturaPuente.nombre_puente.asc()).all()
    return jsonify([lectura.to_dict() for lectura in lecturas])

@usuarios_bp.route("/alertas", methods=["POST"])
def registrar_alerta():
    """POST /alertas → Recibe la medicion enviada por el Arduino y la guarda en Neon."""
    datos = request.get_json()

    if not datos or ("altura_agua" not in datos and "nivel_caudal" not in datos) or "estado_puente" not in datos or not isinstance(datos.get("nombre_puente"), str) or not datos["nombre_puente"].strip():
        return jsonify({"error": "Se requieren nombre_puente, altura_agua (o nivel_caudal) y estado_puente."}), 400

    # Acepta nivel_caudal para mantener compatibilidad con el frontend anterior.
    altura_agua = datos.get("altura_agua", datos.get("nivel_caudal"))

    nombre_puente = datos["nombre_puente"].strip()

    # nombre_puente es la clave estable; la unicidad debe habilitarse en Neon
    # después de revisar y resolver manualmente cualquier duplicado existente.
    lectura = LecturaPuente.query.filter_by(nombre_puente=nombre_puente).with_for_update().first()
    if LecturaPuente.query.filter_by(nombre_puente=nombre_puente).count() > 1:
        return jsonify({"error": "Hay varias filas para este puente; resuelva los duplicados antes de actualizar."}), 409

    valores = dict(
        altura_agua=float(altura_agua),
        altura_puente=float(datos["altura_puente"]) if datos.get("altura_puente") is not None else None,
        estado_puente=datos["estado_puente"]
    )
    if lectura:
        for campo, valor in valores.items():
            setattr(lectura, campo, valor)
        lectura.fecha_registro = db.func.current_timestamp()
        nueva = False
    else:
        lectura = LecturaPuente(nombre_puente=nombre_puente, **valores)
        db.session.add(lectura)
        nueva = True
    db.session.commit()

    return jsonify({
        "mensaje": "Alerta registrada correctamente." if nueva else "Lectura actualizada correctamente.",
        "datos": lectura.to_dict()
    }), 201 if nueva else 200


@usuarios_bp.route("/alertas/ultimo-registro", methods=["GET"])
@usuarios_bp.route("/alertas/estado-actual", methods=["GET"])
def obtener_estado_actual():
    """GET /alertas/estado-actual → Devuelve el registro más reciente para la App Móvil."""
    ultima_lectura = LecturaPuente.query.order_by(LecturaPuente.fecha_registro.desc()).first()

    if ultima_lectura is None:
        return jsonify({"mensaje": "Sin registros de alertas todavía."}), 404

    return jsonify(ultima_lectura.to_dict())

@usuarios_bp.route("/alertas/historial", methods=["GET"])
def obtener_historial_alertas():
    """Devuelve las transiciones de estado almacenadas por el trigger de Neon."""
    historial = HistorialEstadoPuente.query.order_by(HistorialEstadoPuente.fecha_cambio.desc()).all()
    return jsonify([registro.to_dict() for registro in historial])

@usuarios_bp.route("/alertas/<int:alerta_id>", methods=["GET"])
def obtener_alerta_por_id(alerta_id):
    """GET /alertas/1 → busca y devuelve la lectura específica por su id."""
    alerta = db.session.get(LecturaPuente, alerta_id)
    
    if alerta is None:
        return jsonify({"error": "Alerta no encontrada."}), 404
        
    return jsonify(alerta.to_dict()), 200

@usuarios_bp.route("/alertas/<int:alerta_id>", methods=["DELETE"])
def eliminar_alerta(alerta_id):
    alerta = db.session.get(LecturaPuente, alerta_id)
    if alerta is None:
        return jsonify({"error": "Alerta no encontrada."}), 404
    db.session.delete(alerta)
    db.session.commit()
    return jsonify({"mensaje": "Alerta eliminada correctamente."})
