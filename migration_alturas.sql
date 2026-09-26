-- Ejecuta este script en el SQL Editor de Neon antes de desplegar el cambio.
-- Elimina las columnas antiguas de caudal y conserva altura_agua/altura_puente.
CREATE TABLE IF NOT EXISTS lecturas_puente (
    id SERIAL PRIMARY KEY,
    nombre_puente VARCHAR(100) NOT NULL,
    altura_agua DOUBLE PRECISION,
    altura_puente DOUBLE PRECISION,
    estado_puente VARCHAR(20) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE lecturas_puente
    ADD COLUMN IF NOT EXISTS altura_agua DOUBLE PRECISION;

ALTER TABLE lecturas_puente
    ADD COLUMN IF NOT EXISTS altura_puente DOUBLE PRECISION;

-- Conserva los valores anteriores como altura del agua antes de borrar caudal.
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = current_schema()
          AND table_name = 'lecturas_puente'
          AND column_name = 'nivel_caudal'
    ) THEN
        UPDATE lecturas_puente
        SET altura_agua = COALESCE(altura_agua, nivel_caudal);
    END IF;

    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = current_schema()
          AND table_name = 'lecturas_puente'
          AND column_name = 'caudal_historico'
    ) THEN
        UPDATE lecturas_puente
        SET altura_agua = COALESCE(altura_agua, caudal_historico);
    END IF;
END $$;

ALTER TABLE lecturas_puente
    DROP COLUMN IF EXISTS nivel_caudal;

ALTER TABLE lecturas_puente
    DROP COLUMN IF EXISTS caudal_historico;
