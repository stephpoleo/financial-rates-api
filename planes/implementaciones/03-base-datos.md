# [03] Base de Datos - Schema

**Estado**: ⬜ Pendiente
**Dependencias**: [02] Estructura del Proyecto
**Tipo**: 🔴 Secuencial
**Duración estimada**: 30 minutos

## Descripción
Crear base de datos PostgreSQL y schema SQL inicial con todas las tablas necesarias.

## Prerequisitos
- Tarea [02] completada
- PostgreSQL instalado y corriendo

## Archivos a crear
- `database/schema.sql`
- `database/init.sql`

## Pasos de implementación

### 1. Crear base de datos
```bash
# Conectarse a PostgreSQL
psql -U postgres

# Crear base de datos
CREATE DATABASE financial_rates;

# Salir
\q
```

**Si usas Docker:**
```bash
docker exec -it postgres-financial psql -U postgres -c "CREATE DATABASE financial_rates;"
```

### 2. Crear archivo `database/schema.sql`

```sql
-- Archivo: database/schema.sql
-- Schema para Financial Rates API

-- Tabla para CETES
CREATE TABLE cetes (
    id SERIAL PRIMARY KEY,
    plazo INTEGER NOT NULL,  -- 28, 91, 182, 364 días
    tasa DECIMAL(5,2) NOT NULL,
    fecha_subasta DATE NOT NULL,
    fecha_vencimiento DATE,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(plazo, fecha_subasta)
);

-- Tabla para SOFIPOs
CREATE TABLE sofipos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    gat_nominal DECIMAL(5,2),
    gat_real DECIMAL(5,2),
    fecha_actualizacion DATE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tabla para rendimientos por plazo de SOFIPOs
CREATE TABLE sofipo_plazos (
    id SERIAL PRIMARY KEY,
    sofipo_id INTEGER REFERENCES sofipos(id) ON DELETE CASCADE,
    plazo INTEGER NOT NULL,  -- días
    tasa DECIMAL(5,2) NOT NULL,
    fecha_actualizacion DATE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tabla para Fondos/ETFs
CREATE TABLE fondos_etfs (
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
CREATE INDEX idx_cetes_fecha ON cetes(fecha_subasta DESC);
CREATE INDEX idx_cetes_plazo ON cetes(plazo);
CREATE INDEX idx_sofipos_fecha ON sofipos(fecha_actualizacion DESC);
CREATE INDEX idx_sofipos_gat ON sofipos(gat_nominal DESC);
CREATE INDEX idx_sofipo_plazos_sofipo ON sofipo_plazos(sofipo_id);
CREATE INDEX idx_fondos_ticker ON fondos_etfs(ticker);
CREATE INDEX idx_fondos_fecha ON fondos_etfs(fecha_actualizacion DESC);
CREATE INDEX idx_fondos_mercado ON fondos_etfs(mercado);

-- Comentarios para documentación
COMMENT ON TABLE cetes IS 'Tasas históricas de CETES por plazo';
COMMENT ON TABLE sofipos IS 'Información general de SOFIPOs';
COMMENT ON TABLE sofipo_plazos IS 'Rendimientos de SOFIPOs por plazo específico';
COMMENT ON TABLE fondos_etfs IS 'Datos de fondos de inversión y ETFs internacionales';
```

### 3. Ejecutar schema
```bash
psql -U postgres -d financial_rates -f database/schema.sql
```

**Si usas Docker:**
```bash
docker exec -i postgres-financial psql -U postgres -d financial_rates < database/schema.sql
```

### 4. Verificar tablas creadas
```bash
psql -U postgres -d financial_rates -c "\dt"
```

Deberías ver:
```
             List of relations
 Schema |      Name      | Type  |  Owner
--------+----------------+-------+----------
 public | cetes          | table | postgres
 public | fondos_etfs    | table | postgres
 public | sofipo_plazos  | table | postgres
 public | sofipos        | table | postgres
```

### 5. Verificar índices
```bash
psql -U postgres -d financial_rates -c "\di"
```

### 6. Crear archivo `database/init.sql` (opcional)
```sql
-- Archivo: database/init.sql
-- Script para insertar datos de prueba

-- Datos de ejemplo para CETES (febrero 2026)
INSERT INTO cetes (plazo, tasa, fecha_subasta) VALUES
(28, 6.90, '2026-02-03'),
(91, 7.03, '2026-02-03'),
(182, 7.15, '2026-02-03'),
(364, 7.37, '2026-02-03');

-- Este archivo es opcional, solo para testing inicial
```

## Criterios de Aceptación

- [ ] Base de datos `financial_rates` existe
  ```bash
  psql -U postgres -c "\l" | grep financial_rates
  ```

- [ ] Todas las tablas creadas correctamente (4 tablas)
  ```bash
  psql -U postgres -d financial_rates -c "\dt" | wc -l
  ```

- [ ] Índices aplicados (8 índices)
  ```bash
  psql -U postgres -d financial_rates -c "\di"
  ```

- [ ] Constraints funcionando (foreign keys, unique)
  ```bash
  psql -U postgres -d financial_rates -c "\d sofipo_plazos"
  # Debe mostrar Foreign-key constraints
  ```

- [ ] Archivo `database/schema.sql` existe y es ejecutable

## Notas adicionales

- Los tipos `DECIMAL(5,2)` permiten tasas hasta 999.99%
- Los índices mejoran el performance de queries frecuentes
- La constraint `UNIQUE(plazo, fecha_subasta)` previene duplicados en CETES
- `ON DELETE CASCADE` asegura integridad referencial

## Troubleshooting

**Error: "database already exists"**
```bash
psql -U postgres -c "DROP DATABASE financial_rates;"
psql -U postgres -c "CREATE DATABASE financial_rates;"
```

**Error de permisos**
```bash
# Verificar que el usuario postgres tiene permisos
psql -U postgres -c "\du"
```

## Próxima tarea
➡️ [04] Configuración y Environment
