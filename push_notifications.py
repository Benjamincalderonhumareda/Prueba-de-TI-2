"""Web Push delivery for real bridge state transitions."""
import json
import logging
import os
import re
import unicodedata

from models import db, PushSubscription

logger = logging.getLogger(__name__)


def clave_publica_vapid():
    return os.environ.get("VAPID_PUBLIC_KEY", "").strip()


def vapid_configurado():
    return all(os.environ.get(nombre, "").strip() for nombre in (
        "VAPID_PUBLIC_KEY", "VAPID_PRIVATE_KEY", "VAPID_SUBJECT"
    ))


def _normalizar_id_puente(nombre):
    texto = unicodedata.normalize("NFD", str(nombre or ""))
    texto = "".join(caracter for caracter in texto if unicodedata.category(caracter) != "Mn")
    texto = re.sub(r"[^a-zA-Z0-9]", "", texto).lower()
    return texto[6:] if texto.startswith("puente") else texto


def _estado_prioritario(estado):
    texto = unicodedata.normalize("NFD", str(estado or ""))
    texto = "".join(caracter for caracter in texto if unicodedata.category(caracter) != "Mn").lower()
    if "cerr" in texto or "critic" in texto:
        return "Cerrado"
    if "alert" in texto or "precauc" in texto:
        return "Alerta"
    return None


def enviar_notificacion_transicion(nombre_puente, estado_anterior, estado_nuevo):
    """Envía un aviso prioritario a los dispositivos que siguen el puente."""
    estado = _estado_prioritario(estado_nuevo)
    if not estado or str(estado_anterior).strip().casefold() == str(estado_nuevo).strip().casefold():
        return

    private_key = os.environ.get("VAPID_PRIVATE_KEY", "").strip()
    subject = os.environ.get("VAPID_SUBJECT", "").strip()
    if not vapid_configurado():
        logger.warning("Web Push no enviado: falta configurar VAPID_PUBLIC_KEY, VAPID_PRIVATE_KEY o VAPID_SUBJECT.")
        return

    try:
        from pywebpush import WebPushException, webpush
        from py_vapid import Vapid
    except ImportError:
        logger.exception("Web Push no está disponible; instala las dependencias de requirements.txt.")
        return

    clave_privada = Vapid.from_pem(private_key.encode("utf-8")) if "-----BEGIN" in private_key else private_key
    bridge_id = _normalizar_id_puente(nombre_puente)
    payload = json.dumps({
        "title": "Puente cerrado" if estado == "Cerrado" else "Alerta en un puente",
        "body": f"{nombre_puente}: cambió de {estado_anterior} a {estado}.",
        "bridgeId": bridge_id,
        "tag": f"mayualert-{bridge_id}",
    }, ensure_ascii=False)

    suscripciones = PushSubscription.query.filter_by(enabled=True).all()
    hubo_bajas = False
    for registro in suscripciones:
        puentes = registro.bridge_ids if isinstance(registro.bridge_ids, list) else []
        if bridge_id not in {_normalizar_id_puente(item) for item in puentes}:
            continue
        try:
            webpush(
                subscription_info=registro.subscription,
                data=payload,
                vapid_private_key=clave_privada,
                vapid_claims={"sub": subject},
                ttl=3600,
                timeout=10,
            )
        except WebPushException as error:
            status = getattr(getattr(error, "response", None), "status_code", None)
            if status in (404, 410):
                db.session.delete(registro)
                hubo_bajas = True
                logger.info("Suscripción push vencida eliminada (HTTP %s).", status)
            else:
                logger.warning("Falló el envío Web Push (HTTP %s).", status)
        except Exception:
            logger.exception("Falló el envío Web Push para el puente %s.", nombre_puente)

    if hubo_bajas:
        db.session.commit()
