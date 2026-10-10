-- Suscripciones Web Push asociadas al dispositivo/navegador.
-- La clave privada VAPID nunca se almacena en esta tabla ni en Neon.
BEGIN;

CREATE TABLE IF NOT EXISTS push_subscriptions (
    id SERIAL PRIMARY KEY,
    endpoint TEXT NOT NULL UNIQUE,
    subscription JSONB NOT NULL,
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    bridge_ids JSONB NOT NULL DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_push_subscriptions_enabled
    ON push_subscriptions (enabled);

COMMIT;
