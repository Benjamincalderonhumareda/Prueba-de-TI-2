-- Registra en una tabla separada solo los cambios de estado.
-- La tabla lecturas_puente conserva sus filas actuales.
-- Primero inspecciona duplicados con:
-- SELECT nombre_puente, COUNT(*) FROM lecturas_puente GROUP BY nombre_puente HAVING COUNT(*) > 1;
-- Si aparecen filas, decide manualmente cuál conservar y consolida los datos antes
-- de ejecutar esta migración. Este script no borra ni corrige filas automáticamente.

BEGIN;

CREATE TABLE IF NOT EXISTS historial_estados_puente (
    id BIGSERIAL PRIMARY KEY,
    lectura_id INTEGER,
    nombre_puente VARCHAR(100) NOT NULL,
    estado_anterior VARCHAR(20) NOT NULL,
    estado_nuevo VARCHAR(20) NOT NULL,
    datos_anteriores JSONB NOT NULL,
    datos_nuevos JSONB,
    fecha_cambio TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE historial_estados_puente
    ADD COLUMN IF NOT EXISTS datos_nuevos JSONB;

DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM lecturas_puente
        GROUP BY nombre_puente HAVING COUNT(*) > 1
    ) THEN
        RAISE EXCEPTION 'Hay duplicados en lecturas_puente.nombre_puente. Revisa el SELECT comentado y resuélvelos manualmente antes de continuar.';
    END IF;
END $$;

CREATE UNIQUE INDEX IF NOT EXISTS uq_lecturas_puente_nombre
    ON lecturas_puente (nombre_puente);

CREATE OR REPLACE FUNCTION registrar_cambio_estado_puente()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.estado_puente IS DISTINCT FROM NEW.estado_puente THEN
        INSERT INTO historial_estados_puente (
            lectura_id,
            nombre_puente,
            estado_anterior,
            estado_nuevo,
            datos_anteriores,
            datos_nuevos,
            fecha_cambio
        ) VALUES (
            OLD.id,
            OLD.nombre_puente,
            OLD.estado_puente,
            NEW.estado_puente,
            to_jsonb(OLD),
            to_jsonb(NEW),
            CURRENT_TIMESTAMP
        );
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS tr_registrar_cambio_estado_puente ON lecturas_puente;

CREATE TRIGGER tr_registrar_cambio_estado_puente
AFTER UPDATE OF estado_puente ON lecturas_puente
FOR EACH ROW
EXECUTE FUNCTION registrar_cambio_estado_puente();

COMMIT;
