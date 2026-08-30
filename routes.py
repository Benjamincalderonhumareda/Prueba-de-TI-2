# ============================================================================
# routes.py — Los endpoints de la API: qué pasa cuando llega cada petición
# ============================================================================
from flask import Blueprint, request, jsonify
from models import db, Usuario, LecturaPuente

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

@usuarios_bp.route("/alertas", methods=["POST"])
def registrar_alerta():
    """POST /alertas → Recibe la medicion enviada por el Arduino y la guarda en Neon."""
    datos = request.get_json()

    if not datos or "nivel_caudal" not in datos or "estado_puente" not in datos:
        return jsonify({"error": "Faltan datos obligatorios (nivel_caudal, estado_puente)."}), 400

    nueva_lectura = LecturaPuente(
        nombre_puente=datos.get("nombre_puente", "Puente Carapongo"),
        nivel_caudal=float(datos["nivel_caudal"]),
        estado_puente=datos["estado_puente"]
    )

    db.session.add(nueva_lectura)
    db.session.commit()

    return jsonify({
        "mensaje": "Alerta registrada correctamente.",
        "datos": nueva_lectura.to_dict()
    }), 201


@usuarios_bp.route("/alertas/estado-actual", methods=["GET"])
def obtener_estado_actual():
    """GET /alertas/estado-actual → Devuelve el registro mas reciente para la App Movil."""
    ultima_lectura = LecturaPuente.query.order_by(LecturaPuente.fecha_registro.desc()).first()

    if ultima_lectura is None:
        return jsonify({"mensaje": "Sin registros de alertas todavia."}), 404

    return jsonify(ultima_lectura.to_dict())
