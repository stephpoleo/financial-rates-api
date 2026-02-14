-- Financial Rates API - Schema de Base de Datos
-- Ejecutar: psql -U postgres -d financial_rates -f database/schema.sql

-- Tabla para CETES
CREATE TABLE IF NOT EXISTS cetes (
    id SERIAL PRIMARY KEY,
    plazo INTEGER NOT NULL,  -- 28, 91, 182, 364 días
    tasa DECIMAL(5,2) NOT NULL,
    fecha_subasta DATE NOT NULL,
    fecha_vencimiento DATE,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(plazo, fecha_subasta)
);

-- Tabla para SOFIPOs
CREATE TABLE IF NOT EXISTS sofipos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    gat_nominal DECIMAL(5,2),
    gat_real DECIMAL(5,2),
    fecha_actualizacion DATE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tabla para rendimientos por plazo de SOFIPOs
CREATE TABLE IF NOT EXISTS sofipo_plazos (
    id SERIAL PRIMARY KEY,
    sofipo_id INTEGER REFERENCES sofipos(id) ON DELETE CASCADE,
    plazo INTEGER NOT NULL,  -- días
    tasa DECIMAL(5,2) NOT NULL,
    fecha_actualizacion DATE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tabla para Fondos/ETFs
CREATE TABLE IF NOT EXISTS fondos_etfs (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(20) NOT NULL,
    nombre VARCHAR(200),
    tipo VARCHAR(50),  -- 'ETF', 'MUTUAL_FUND', etc.
    mercado VARCHAR(50),  -- 'US', 'MX', 'EU', etc.
    precio_actual DECIMAL(10,2),
    rendimiento_anual DECIMAL(5,2),
    rendimiento_ytd DECIMAL(5,2),
    fecha_actualizacion DATE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(ticker, fecha_actualizacion)
);

-- Índices para optimizar consultas
CREATE INDEX IF NOT EXISTS idx_cetes_fecha ON cetes(fecha_subasta DESC);
CREATE INDEX IF NOT EXISTS idx_cetes_plazo ON cetes(plazo);
CREATE INDEX IF NOT EXISTS idx_sofipos_fecha ON sofipos(fecha_actualizacion DESC);
CREATE INDEX IF NOT EXISTS idx_sofipo_plazos_sofipo ON sofipo_plazos(sofipo_id);
CREATE INDEX IF NOT EXISTS idx_fondos_ticker ON fondos_etfs(ticker);
CREATE INDEX IF NOT EXISTS idx_fondos_fecha ON fondos_etfs(fecha_actualizacion DESC);
CREATE INDEX IF NOT EXISTS idx_fondos_tipo ON fondos_etfs(tipo);
CREATE INDEX IF NOT EXISTS idx_fondos_mercado ON fondos_etfs(mercado);
