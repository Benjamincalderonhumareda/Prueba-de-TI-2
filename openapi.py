"""Especificación OpenAPI que consume Swagger UI."""

OPENAPI_SPEC = {
    "openapi": "3.0.3",
    "info": {
        "title": "API Mayu",
        "version": "1.0.0",
        "description": "API REST de monitoreo de puentes MayuAlert.",
    },
    "servers": [{"url": "/", "description": "Servidor actual"}],
    "tags": [
        {"name": "Alertas"},
        {"name": "Notificaciones"},
    ],
    "paths": {
        "/alertas": {
            "get": {"tags": ["Alertas"], "summary": "Lista las lecturas actuales, una por puente", "responses": {"200": {"description": "Lecturas actuales", "content": {"application/json": {"schema": {"type": "array", "items": {"$ref": "#/components/schemas/Alerta"}}}}}}},
            "post": {"tags": ["Alertas"], "summary": "Registra una lectura", "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/NuevaAlerta"}}}}, "responses": {"201": {"description": "Lectura registrada"}, "400": {"description": "Faltan campos obligatorios"}}},
        },
        "/alertas/estado-actual": {"get": {"tags": ["Alertas"], "summary": "Obtiene la lectura más reciente", "responses": {"200": {"description": "Lectura actual", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Alerta"}}}}, "404": {"description": "Sin registros"}}}},
        "/alertas/ultimo-registro": {"get": {"tags": ["Alertas"], "summary": "Alias de estado actual", "responses": {"200": {"description": "Lectura actual"}, "404": {"description": "Sin registros"}}}},
        "/alertas/historial": {"get": {"tags": ["Alertas"], "summary": "Lista transiciones de estado por fecha descendente", "responses": {"200": {"description": "Transiciones registradas por Neon", "content": {"application/json": {"schema": {"type": "array", "items": {"$ref": "#/components/schemas/HistorialEstadoPuente"}}}}}}}},
        "/notificaciones/clave-publica": {
            "get": {
                "tags": ["Notificaciones"],
                "summary": "Devuelve la clave pública VAPID para el navegador",
                "responses": {
                    "200": {
                        "description": "Clave pública VAPID",
                        "content": {"application/json": {"schema": {
                            "type": "object",
                            "properties": {"publicKey": {"type": "string"}},
                        }}},
                    },
                    "503": {"description": "Web Push no está configurado"},
                },
            },
        },
        "/notificaciones/suscripciones": {
            "post": {
                "tags": ["Notificaciones"],
                "summary": "Registra o actualiza una suscripción por dispositivo",
                "requestBody": {"required": True, "content": {"application/json": {
                    "schema": {"$ref": "#/components/schemas/NuevaSuscripcionPush"},
                }}},
                "responses": {
                    "200": {"description": "Suscripción actualizada"},
                    "201": {"description": "Suscripción creada"},
                    "400": {"description": "Suscripción inválida"},
                },
            },
            "delete": {
                "tags": ["Notificaciones"],
                "summary": "Retira la suscripción del dispositivo",
                "requestBody": {"required": True, "content": {"application/json": {
                    "schema": {"type": "object", "required": ["endpoint"], "properties": {
                        "endpoint": {"type": "string", "format": "uri"},
                    }},
                }}},
                "responses": {
                    "200": {"description": "Suscripción retirada"},
                    "400": {"description": "Endpoint inválido"},
                },
            },
        },
        "/alertas/{alerta_id}": {
            "parameters": [{"name": "alerta_id", "in": "path", "required": True, "schema": {"type": "integer"}}],
            "get": {"tags": ["Alertas"], "summary": "Busca una lectura por ID", "responses": {"200": {"description": "Lectura encontrada", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Alerta"}}}}, "404": {"description": "Lectura no encontrada"}}},
            "delete": {"tags": ["Alertas"], "summary": "Elimina una lectura", "responses": {"200": {"description": "Lectura eliminada"}, "404": {"description": "Lectura no encontrada"}}},
        },
    },
    "components": {
        "schemas": {
            "NuevaSuscripcionPush": {
                "type": "object",
                "required": ["subscription"],
                "properties": {
                    "subscription": {
                        "type": "object",
                        "required": ["endpoint", "keys"],
                        "properties": {
                            "endpoint": {"type": "string", "format": "uri"},
                            "keys": {
                                "type": "object",
                                "required": ["p256dh", "auth"],
                                "properties": {
                                    "p256dh": {"type": "string"},
                                    "auth": {"type": "string"},
                                },
                            },
                        },
                    },
                    "enabled": {"type": "boolean", "default": True},
                    "bridges": {"type": "array", "items": {"type": "string"}},
                },
            },
            "Alerta": {"type": "object", "properties": {"id": {"type": "integer"}, "nombre_puente": {"type": "string"}, "altura_agua": {"type": "number", "nullable": True, "description": "Altura del agua en metros"}, "altura_puente": {"type": "number", "nullable": True, "description": "Altura del puente en metros"}, "estado_puente": {"type": "string"}, "fecha_registro": {"type": "string"}}},
            "HistorialEstadoPuente": {"type": "object", "required": ["nombre_puente", "estado_anterior", "estado_nuevo", "fecha_cambio"], "properties": {"id": {"type": "integer"}, "lectura_id": {"type": "integer", "nullable": True}, "nombre_puente": {"type": "string"}, "estado_anterior": {"type": "string"}, "estado_nuevo": {"type": "string"}, "datos_anteriores": {"type": "object"}, "datos_nuevos": {"type": "object", "nullable": True}, "fecha_cambio": {"type": "string", "format": "date-time"}}},
            "NuevaAlerta": {"type": "object", "required": ["nombre_puente", "estado_puente"], "description": "Envía altura_agua o nivel_caudal (alias compatible con el frontend anterior). nombre_puente identifica de forma estable la fila actual del puente.", "properties": {"nombre_puente": {"type": "string", "example": "Puente Carapongo"}, "altura_agua": {"type": "number", "example": 1.25, "description": "Altura del agua en metros"}, "nivel_caudal": {"type": "number", "deprecated": True, "example": 1.25, "description": "Alias de entrada para compatibilidad; se guarda como altura_agua"}, "altura_puente": {"type": "number", "nullable": True, "example": 5.0, "description": "Altura del puente en metros; opcional mientras esté pendiente"}, "estado_puente": {"type": "string", "example": "normal"}}},
        }
    },
}
