# API MayuAlert

API REST para monitorear puentes del rio Rimac. El backend usa Flask y Neon PostgreSQL.

## Datos principales

- `lecturas_puente`: ultima lectura y estado actual de cada puente.
- `historial_estados_puente`: cambios de estado registrados por un trigger de Neon.
- `push_subscriptions`: dispositivos y puentes seleccionados para recibir avisos Web Push.

La API tambien contiene endpoints de alertas para registrar y consultar lecturas. Las notificaciones push se envian cuando una lectura cambia a un estado critico. La aplicacion web consulta los datos actuales desde `/alertas` y el historial desde `/alertas/historial`.

## Ejecutar localmente

1. Crear y activar un entorno virtual.
2. Instalar dependencias con `pip install -r requirements.txt`.
3. Copiar `.env.example` a `.env` y configurar `DATABASE_URL`.
4. Para Web Push, configurar `VAPID_PUBLIC_KEY`, `VAPID_PRIVATE_KEY` y `VAPID_SUBJECT`.
5. Ejecutar `python run.py`.

Swagger UI queda en `http://127.0.0.1:5001/docs/` y OpenAPI en `http://127.0.0.1:5001/openapi.json`.

## Endpoints

| Metodo | Ruta | Funcion |
| --- | --- | --- |
| GET | `/alertas` | Lista la lectura actual de cada puente. |
| POST | `/alertas` | Registra o actualiza una lectura del sensor. |
| GET | `/alertas/estado-actual` | Obtiene la lectura mas reciente. |
| GET | `/alertas/historial` | Lista transiciones de estado. |
| GET, DELETE | `/alertas/<id>` | Consulta o elimina una lectura. |
| GET | `/notificaciones/clave-publica` | Entrega la clave publica VAPID. |
| POST, DELETE | `/notificaciones/suscripciones` | Registra o retira un dispositivo push. |

## Neon y Render

Neon guarda las lecturas, el historial y las suscripciones. Render ejecuta el backend con las variables de entorno configuradas en el servicio. La tabla de historial depende de las migraciones SQL documentadas para Neon; `db.create_all()` por si solo no crea sus triggers.
