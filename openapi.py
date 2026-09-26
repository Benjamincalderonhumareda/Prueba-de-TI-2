"""Especificación OpenAPI que consume Swagger UI."""

OPENAPI_SPEC = {
    "openapi": "3.0.3",
    "info": {
        "title": "API Mayu",
        "version": "1.0.0",
        "description": "API REST de usuarios y lecturas del puente.",
    },
    "servers": [{"url": "/", "description": "Servidor actual"}],
    "tags": [
        {"name": "Usuarios"},
        {"name": "Alertas"},
    ],
    "paths": {
        "/usuarios": {
            "get": {
                "tags": ["Usuarios"], "summary": "Lista los usuarios",
                "responses": {"200": {"description": "Lista de usuarios", "content": {"application/json": {"schema": {"type": "array", "items": {"$ref": "#/components/schemas/Usuario"}}}}}},
            },
            "post": {
                "tags": ["Usuarios"], "summary": "Crea un usuario",
                "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/NuevoUsuario"}}}},
                "responses": {"201": {"description": "Usuario creado", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Usuario"}}}}, "400": {"description": "Datos inválidos"}, "409": {"description": "El email ya existe"}},
            },
        },
        "/usuarios/{usuario_id}": {
            "parameters": [{"name": "usuario_id", "in": "path", "required": True, "schema": {"type": "integer"}}],
            "get": {"tags": ["Usuarios"], "summary": "Busca usuario por ID", "responses": {"200": {"description": "Usuario encontrado", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Usuario"}}}}, "404": {"description": "Usuario no encontrado"}}},
            "put": {"tags": ["Usuarios"], "summary": "Actualiza un usuario", "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ActualizarUsuario"}}}}, "responses": {"200": {"description": "Usuario actualizado"}, "404": {"description": "Usuario no encontrado"}}},
            "delete": {"tags": ["Usuarios"], "summary": "Elimina un usuario", "responses": {"200": {"description": "Usuario eliminado"}, "404": {"description": "Usuario no encontrado"}}},
        },
        "/alertas": {
            "post": {"tags": ["Alertas"], "summary": "Registra una lectura", "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/NuevaAlerta"}}}}, "responses": {"201": {"description": "Lectura registrada"}, "400": {"description": "Faltan campos obligatorios"}}},
        },
        "/alertas/estado-actual": {"get": {"tags": ["Alertas"], "summary": "Obtiene la lectura más reciente", "responses": {"200": {"description": "Lectura actual", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Alerta"}}}}, "404": {"description": "Sin registros"}}}},
        "/alertas/ultimo-registro": {"get": {"tags": ["Alertas"], "summary": "Alias de estado actual", "responses": {"200": {"description": "Lectura actual"}, "404": {"description": "Sin registros"}}}},
        "/alertas/historial": {"get": {"tags": ["Alertas"], "summary": "Lista todas las lecturas", "responses": {"200": {"description": "Historial", "content": {"application/json": {"schema": {"type": "array", "items": {"$ref": "#/components/schemas/Alerta"}}}}}}}},
        "/alertas/{alerta_id}": {
            "parameters": [{"name": "alerta_id", "in": "path", "required": True, "schema": {"type": "integer"}}],
            "get": {"tags": ["Alertas"], "summary": "Busca una lectura por ID", "responses": {"200": {"description": "Lectura encontrada", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Alerta"}}}}, "404": {"description": "Lectura no encontrada"}}},
            "delete": {"tags": ["Alertas"], "summary": "Elimina una lectura", "responses": {"200": {"description": "Lectura eliminada"}, "404": {"description": "Lectura no encontrada"}}},
        },
    },
    "components": {
        "schemas": {
            "Usuario": {"type": "object", "properties": {"id": {"type": "integer"}, "nombre": {"type": "string"}, "email": {"type": "string", "format": "email"}, "edad": {"type": "integer", "nullable": True}}},
            "NuevoUsuario": {"type": "object", "required": ["nombre", "email"], "properties": {"nombre": {"type": "string", "example": "Ana Torres"}, "email": {"type": "string", "format": "email", "example": "ana@example.com"}, "edad": {"type": "integer", "nullable": True, "example": 25}}},
            "ActualizarUsuario": {"type": "object", "properties": {"nombre": {"type": "string"}, "email": {"type": "string", "format": "email"}, "edad": {"type": "integer", "nullable": True}}},
            "Alerta": {"type": "object", "properties": {"id": {"type": "integer"}, "nombre_puente": {"type": "string"}, "altura_agua": {"type": "number", "nullable": True, "description": "Altura del agua en metros"}, "nivel_caudal": {"type": "number", "nullable": True, "deprecated": True, "description": "Alias de compatibilidad; contiene altura_agua en metros"}, "altura_puente": {"type": "number", "nullable": True, "description": "Altura del puente en metros"}, "estado_puente": {"type": "string"}, "fecha_registro": {"type": "string"}}},
            "NuevaAlerta": {"type": "object", "required": ["estado_puente"], "description": "Envía altura_agua o nivel_caudal (alias compatible con el frontend anterior). Ambos representan la altura del agua en metros.", "properties": {"nombre_puente": {"type": "string", "example": "Puente Carapongo"}, "altura_agua": {"type": "number", "example": 1.25, "description": "Altura del agua en metros"}, "nivel_caudal": {"type": "number", "deprecated": True, "example": 1.25, "description": "Alias de entrada para compatibilidad; se guarda como altura_agua"}, "altura_puente": {"type": "number", "nullable": True, "example": 5.0, "description": "Altura del puente en metros; opcional mientras esté pendiente"}, "estado_puente": {"type": "string", "example": "normal"}}},
        }
    },
}
