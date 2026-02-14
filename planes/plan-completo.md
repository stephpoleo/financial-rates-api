# Sistema de Monitoreo de Rendimientos Financieros

## Resumen
Sistema Python que recopila diariamente rendimientos de CETES, SOFIPOs, fondos de inversión y ETFs (mexicanos e internacionales), los almacena en base de datos y expone una API REST para consultas.

## Estructura de Organización del Proyecto

Este plan está diseñado para ser modular y organizado. La implementación se divide en sub-tareas independientes que permiten trabajo paralelo donde sea posible.

```
financial-rates-api/
├── planes/                          # Documentación de planificación
│   ├── plan-completo.md            # Este documento (plan maestro)
│   └── implementaciones/            # Sub-tareas individuales
│       ├── LEEME.md                # Índice y grafo de dependencias
│       ├── 01-setup-inicial.md
│       ├── 02-estructura-proyecto.md
│       ├── 03-base-datos.md
│       ├── 04-config-env.md
│       ├── 05-models-cetes.md
│       ├── 06-models-sofipos.md
│       ├── 07-models-fondos.md
│       ├── 08-collector-banxico.md
│       ├── 09-collector-sofipos.md
│       ├── 10-collector-etfs.md
│       ├── 11-scheduler.md
│       ├── 12-api-cetes.md
│       ├── 13-api-sofipos.md
│       ├── 14-api-fondos.md
│       ├── 15-api-comparar.md
│       ├── 16-tests.md
│       └── 17-docker-deploy.md
└── [resto de archivos del proyecto...]
```

## Grafo de Dependencias e Implementaciones

### Leyenda
- 🟢 **Paralelo**: Se puede trabajar simultáneamente con otras tareas
- 🔴 **Secuencial**: Requiere que otras tareas estén completas primero
- ⏱️ **Duración estimada**: Tiempo aproximado de implementación

### Grafo de Dependencias

```
┌─────────────────────────────────────────────────────────────┐
│                         NIVEL 1                             │
│              (Fundación - Secuencial)                       │
├─────────────────────────────────────────────────────────────┤
│  [01] Setup Inicial                                         │
│    └──> [02] Estructura Proyecto                            │
│          └──> [03] Base de Datos (Schema SQL)               │
│                └──> [04] Config & Environment               │
└──────────────────────────┬──────────────────────────────────┘
                           │
      ┌────────────────────┼────────────────────┐
      │                    │                    │
┌─────▼──────────┐  ┌──────▼───────┐  ┌────────▼─────────┐
│   NIVEL 2      │  │   NIVEL 2    │  │    NIVEL 2       │
│  (Paralelo)    │  │  (Paralelo)  │  │   (Paralelo)     │
├────────────────┤  ├──────────────┤  ├──────────────────┤
│ [05] Model     │  │ [06] Model   │  │ [07] Model       │
│     CETES      │  │    SOFIPOs   │  │    Fondos/ETFs   │
└───────┬────────┘  └──────┬───────┘  └────────┬─────────┘
        │                  │                    │
┌───────▼────────┐  ┌──────▼───────┐  ┌────────▼─────────┐
│   NIVEL 3      │  │   NIVEL 3    │  │    NIVEL 3       │
│  (Paralelo)    │  │  (Paralelo)  │  │   (Paralelo)     │
├────────────────┤  ├──────────────┤  ├──────────────────┤
│ [08] Collector │  │ [09] Scraper │  │ [10] Collector   │
│    Banxico     │  │   SOFIPOs    │  │      ETFs        │
└───────┬────────┘  └──────┬───────┘  └────────┬─────────┘
        │                  │                    │
        └──────────────────┼────────────────────┘
                           │
                     ┌─────▼──────┐
                     │  NIVEL 4   │
                     │(Secuencial)│
                     ├────────────┤
                     │    [11]    │
                     │ Scheduler  │
                     └─────┬──────┘
                           │
      ┌────────────────────┼────────────────────┐
      │                    │                    │
┌─────▼──────────┐  ┌──────▼───────┐  ┌────────▼─────────┐
│   NIVEL 5      │  │   NIVEL 5    │  │    NIVEL 5       │
│  (Paralelo)    │  │  (Paralelo)  │  │   (Paralelo)     │
├────────────────┤  ├──────────────┤  ├──────────────────┤
│ [12] Router    │  │ [13] Router  │  │ [14] Router      │
│     CETES      │  │    SOFIPOs   │  │    Fondos        │
└───────┬────────┘  └──────┬───────┘  └────────┬─────────┘
        │                  │                    │
        └──────────────────┼────────────────────┘
                           │
                     ┌─────▼──────┐
                     │  NIVEL 6   │
                     │ (Paralelo) │
                     ├────────────┤
                     │    [15]    │
                     │   Router   │
                     │  Comparar  │
                     └─────┬──────┘
                           │
      ┌────────────────────┴────────────────────┐
      │                                         │
┌─────▼──────────┐                    ┌─────────▼────────┐
│   NIVEL 7      │                    │    NIVEL 7       │
│  (Paralelo)    │                    │   (Paralelo)     │
├────────────────┤                    ├──────────────────┤
│ [16] Tests &   │                    │ [17] Docker &    │
│  Documentation │                    │   Deployment     │
└────────────────┘                    └──────────────────┘
```

### Resumen de Niveles de Paralelización

| Nivel | Tareas | Tipo | Descripción |
|-------|--------|------|-------------|
| **1** | 01-04 | 🔴 Secuencial | Fundación del proyecto, debe hacerse en orden |
| **2** | 05-07 | 🟢 Paralelo | Modelos de base de datos, independientes entre sí |
| **3** | 08-10 | 🟢 Paralelo | Collectors/scrapers, independientes entre sí |
| **4** | 11 | 🔴 Secuencial | Scheduler que orquesta los collectors |
| **5** | 12-14 | 🟢 Paralelo | Routers API básicos, independientes entre sí |
| **6** | 15 | 🔴 Secuencial | Router de comparación (usa los otros routers) |
| **7** | 16-17 | 🟢 Paralelo | Testing y deployment, pueden ir simultáneamente |

### Estrategia de Implementación Sugerida

**Sprint 1 - Fundación (Nivel 1)**
- Días 1-2: Implementar tareas 01-04 secuencialmente
- Resultado: Proyecto configurado con DB lista

**Sprint 2 - Modelos (Nivel 2)**
- Día 3: Implementar tareas 05, 06, 07 en paralelo (3 personas) o secuencialmente (1 persona)
- Resultado: Modelos de datos completos

**Sprint 3 - Recopiladores (Nivel 3)**
- Días 4-5: Implementar tareas 08, 09, 10 en paralelo o secuencialmente
- Resultado: Datos fluyendo a la base de datos

**Sprint 4 - Orquestación (Nivel 4)**
- Día 6: Implementar tarea 11
- Resultado: Sistema automatizado de recopilación

**Sprint 5 - API (Niveles 5-6)**
- Día 7: Implementar tareas 12, 13, 14 en paralelo
- Día 8: Implementar tarea 15
- Resultado: API REST completa y funcional

**Sprint 6 - Finalización (Nivel 7)**
- Días 9-10: Implementar tareas 16 y 17 en paralelo
- Resultado: Sistema testeado y deployable

## Arquitectura General

```
┌─────────────────────────────────────────────────────────┐
│                  Recopiladores de Datos                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Banxico API  │  │ Web Scrapers │  │   ETF APIs   │  │
│  │   (CETES)    │  │  (SOFIPOs)   │  │ (Internac.)  │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
│         │                  │                  │          │
│         └──────────────────┴──────────────────┘          │
│                            │                             │
└────────────────────────────┼─────────────────────────────┘
                             ▼
                   ┌─────────────────┐
                   │  PostgreSQL DB  │
                   │   - CETES       │
                   │   - SOFIPOs     │
                   │   - Fondos/ETFs │
                   └────────┬────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │   FastAPI REST  │
                   │   - GET rates   │
                   │   - Compare     │
                   │   - Historical  │
                   └─────────────────┘
```

## Fuentes de Datos

### 1. CETES - API Oficial de Banxico ✅
- **Fuente**: Sistema de Información Económica (SIE) de Banxico
- **Método**: API REST oficial con autenticación por token
- **Endpoint**: `https://www.banxico.org.mx/SieAPIRest/service/v1/series/{series}/datos`
- **Series necesarias** (IDs de Banxico):
  - CETES 28 días: `SF43936`
  - CETES 91 días: `SF43939`
  - CETES 182 días: `SF43942`
  - CETES 364 días: `SF43945`
- **Librería Python**: `sie-banxico` o `requests` directo
- **Formato**: JSON
- **Frecuencia de actualización**: Diaria después de cada subasta (usualmente martes)

### 2. SOFIPOs - Web Scraping 🕷️
- **Fuente primaria**: [Tasas.mx](https://www.tasas.mx/) o [ComparaSOFIPOS](https://comparasofipos.com/)
- **Método**: Web scraping con BeautifulSoup/Scrapy
- **Datos a extraer**:
  - Nombre de la SOFIPO
  - Rendimiento a la vista (GAT nominal y real)
  - Rendimientos por plazo (28, 91, 180, 360 días)
  - Fecha de actualización
- **Herramientas**: BeautifulSoup4 + requests (o Selenium si hay JS dinámico)
- **Frecuencia de actualización**: Diaria

### 3. Fondos de Inversión y ETFs Internacionales - APIs Comerciales 🌍
Opciones de APIs (elegir según presupuesto):

**Opción A - Alpha Vantage (Recomendada para empezar)**
- **Tier gratuito**: 25 requests/día, suficiente para pruebas
- **Cobertura**: Stocks, ETFs, fondos globales
- **Endpoint**: `https://www.alphavantage.co/query`
- **Documentación**: https://www.alphavantage.co/documentation/

**Opción B - Twelve Data**
- **Tier gratuito**: 800 requests/día
- **Cobertura**: ETFs de múltiples mercados globales
- **Formato**: JSON, WebSocket para real-time

**Opción C - EOD Historical Data**
- **Cobertura**: 30+ años de historia, 45,000+ fondos mutuos
- **Pricing**: Desde $20/mes

## Stack Tecnológico

### Backend
- **Python 3.11+**
- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy 2.0**: ORM para manejo de base de datos
- **Alembic**: Migraciones de base de datos

### Scraping & APIs
- **requests**: Cliente HTTP para APIs
- **BeautifulSoup4**: Parser HTML para scraping simple
- **Scrapy** (opcional): Si se necesita scraping más robusto
- **Selenium** (opcional): Si los sitios tienen mucho JavaScript

### Base de Datos
- **PostgreSQL**: Base de datos relacional robusta
- **Alternativa**: SQLite para desarrollo/pruebas

### Task Scheduling
- **APScheduler**: Scheduler para tareas periódicas en Python
- **Alternativa**: Celery + Redis (si se requiere mayor escalabilidad)

### Utilidades
- **pydantic**: Validación de datos
- **python-dotenv**: Manejo de variables de entorno
- **loguru**: Logging mejorado

## Estructura de Base de Datos

```sql
-- Tabla para CETES
CREATE TABLE cetes (
    id SERIAL PRIMARY KEY,
    plazo INTEGER NOT NULL,  -- 28, 91, 182, 364
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
    sofipo_id INTEGER REFERENCES sofipos(id),
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
CREATE INDEX idx_sofipos_fecha ON sofipos(fecha_actualizacion DESC);
CREATE INDEX idx_fondos_ticker ON fondos_etfs(ticker);
CREATE INDEX idx_fondos_fecha ON fondos_etfs(fecha_actualizacion DESC);
```

## Estructura del Proyecto

```
financial-rates-api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app
│   ├── config.py               # Configuración y env vars
│   ├── database.py             # Conexión DB y setup
│   │
│   ├── models/                 # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── cetes.py
│   │   ├── sofipos.py
│   │   └── fondos.py
│   │
│   ├── schemas/                # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── cetes.py
│   │   ├── sofipos.py
│   │   └── fondos.py
│   │
│   ├── collectors/             # Recopiladores de datos
│   │   ├── __init__.py
│   │   ├── banxico_collector.py    # API Banxico
│   │   ├── sofipo_scraper.py       # Scraper SOFIPOs
│   │   └── etf_collector.py        # API ETFs
│   │
│   ├── routers/                # API endpoints
│   │   ├── __init__.py
│   │   ├── cetes.py
│   │   ├── sofipos.py
│   │   └── fondos.py
│   │
│   └── scheduler.py            # APScheduler config
│
├── alembic/                    # Migraciones DB
│   └── versions/
├── tests/                      # Tests
├── .env.example
├── requirements.txt
├── Dockerfile
└── README.md
```

## Plan de Implementación

### Fase 1: Setup Inicial
1. Crear estructura del proyecto
2. Configurar entorno virtual Python
3. Instalar dependencias base (`requirements.txt`)
4. Configurar PostgreSQL y crear base de datos
5. Setup de variables de entorno (`.env`)

### Fase 2: Base de Datos
1. Definir modelos SQLAlchemy (`app/models/`)
2. Configurar Alembic para migraciones
3. Crear migración inicial con tablas
4. Aplicar migración y verificar esquema

### Fase 3: Recopiladores de Datos

**3.1 - CETES (Banxico API)**
1. Registrarse en Banxico SIE y obtener token
2. Implementar `banxico_collector.py`:
   - Cliente para API de Banxico
   - Funciones para obtener series de CETES
   - Parser de respuestas JSON
   - Guardado en base de datos
3. Crear pruebas unitarias
4. Definir schemas Pydantic para validación

**3.2 - SOFIPOs (Web Scraping)**
1. Analizar estructura HTML de Tasas.mx
2. Implementar `sofipo_scraper.py`:
   - Scraper con BeautifulSoup/requests
   - Extracción de rendimientos a la vista
   - Extracción de rendimientos por plazo
   - Manejo de errores y rate limiting
3. Implementar guardado en base de datos
4. Crear pruebas

**3.3 - Fondos/ETFs (API Externa)**
1. Elegir proveedor de API (Alpha Vantage para empezar)
2. Obtener API key
3. Implementar `etf_collector.py`:
   - Cliente HTTP para la API
   - Funciones para buscar fondos por ticker
   - Parser de rendimientos y precios
   - Guardado en base de datos
4. Definir lista inicial de tickers a monitorear
5. Crear pruebas

### Fase 4: Scheduler
1. Implementar `scheduler.py` con APScheduler
2. Configurar jobs diarios:
   - CETES: 11:00 AM (después de subasta)
   - SOFIPOs: 7:00 AM
   - ETFs: 8:00 PM (después del cierre de mercados)
3. Implementar logging de ejecuciones
4. Manejo de errores y reintentos

### Fase 5: API REST (FastAPI)
1. Implementar schemas Pydantic de respuesta
2. Crear endpoints en `routers/`:

   **CETES:**
   - `GET /api/cetes` - Listar todas las tasas actuales
   - `GET /api/cetes/{plazo}` - Tasa actual por plazo
   - `GET /api/cetes/historico` - Serie histórica

   **SOFIPOs:**
   - `GET /api/sofipos` - Listar todas las SOFIPOs
   - `GET /api/sofipos/{id}` - Detalle de SOFIPO con todos sus plazos
   - `GET /api/sofipos/comparar` - Comparar rendimientos

   **Fondos/ETFs:**
   - `GET /api/fondos` - Listar fondos (con filtros por tipo, mercado)
   - `GET /api/fondos/{ticker}` - Detalle de fondo específico
   - `GET /api/fondos/buscar?q={query}` - Búsqueda por nombre/ticker

   **Comparación:**
   - `GET /api/comparar` - Comparar CETES vs SOFIPOs vs Fondos

3. Documentación automática OpenAPI/Swagger
4. Implementar paginación y filtros
5. Agregar CORS headers

### Fase 6: Testing & Documentación
1. Crear tests de integración
2. Escribir README con:
   - Instrucciones de setup
   - Cómo obtener API keys
   - Ejemplos de uso de la API
3. Documentar endpoints en detalle

### Fase 7: Deployment (Opcional)
1. Crear Dockerfile
2. Docker Compose con PostgreSQL
3. Configurar para producción (gunicorn/uvicorn)
4. Variables de entorno de producción

## Archivos Críticos

- `app/config.py` - Configuración centralizada con variables de entorno
- `app/database.py` - Setup de SQLAlchemy y sesiones
- `app/collectors/banxico_collector.py` - Recopilador de CETES
- `app/collectors/sofipo_scraper.py` - Scraper de SOFIPOs
- `app/collectors/etf_collector.py` - Recopilador de fondos/ETFs
- `app/scheduler.py` - Programación de tareas diarias
- `app/main.py` - Aplicación FastAPI principal
- `requirements.txt` - Dependencias del proyecto
- `alembic/versions/` - Migraciones de base de datos

## Verificación End-to-End

### 1. Verificar Recopilación de Datos
```bash
# Ejecutar manualmente cada recopilador
python -m app.collectors.banxico_collector
python -m app.collectors.sofipo_scraper
python -m app.collectors.etf_collector

# Verificar datos en DB
psql -d financial_rates -c "SELECT * FROM cetes ORDER BY fecha_subasta DESC LIMIT 5;"
psql -d financial_rates -c "SELECT * FROM sofipos ORDER BY fecha_actualizacion DESC LIMIT 5;"
psql -d financial_rates -c "SELECT * FROM fondos_etfs ORDER BY fecha_actualizacion DESC LIMIT 5;"
```

### 2. Verificar Scheduler
```bash
# Iniciar scheduler en modo test
python -m app.scheduler

# Verificar logs para confirmar ejecución de jobs
tail -f logs/scheduler.log
```

### 3. Verificar API
```bash
# Iniciar servidor FastAPI
uvicorn app.main:app --reload

# Probar endpoints
curl http://localhost:8000/api/cetes
curl http://localhost:8000/api/sofipos
curl http://localhost:8000/api/fondos?mercado=US
curl http://localhost:8000/api/comparar

# Revisar documentación automática
# Abrir navegador: http://localhost:8000/docs
```

### 4. Ejecutar Tests
```bash
# Tests unitarios
pytest tests/unit/

# Tests de integración
pytest tests/integration/

# Coverage
pytest --cov=app tests/
```

### 5. Verificar Performance
```bash
# Medir tiempo de respuesta de endpoints
time curl http://localhost:8000/api/cetes
time curl http://localhost:8000/api/sofipos
```

## Consideraciones Importantes

### Seguridad
- **API Keys**: Nunca commitear keys en el código, usar `.env`
- **Rate Limiting**: Implementar límites en la API para prevenir abuso
- **CORS**: Configurar correctamente para frontend si es necesario

### Web Scraping Ético
- **Respetar robots.txt** de los sitios
- **Rate limiting**: Espaciar requests (ej: 1-2 segundos entre requests)
- **User-Agent**: Identificarse apropiadamente
- **Caching**: No hacer scraping excesivo, guardar resultados

### Escalabilidad Futura
- Si se agregan muchos más fondos/ETFs, considerar:
  - Celery + Redis para tareas asíncronas
  - Caché con Redis para endpoints frecuentes
  - Particionamiento de tablas por fecha

### Monitoreo
- Implementar logging robusto con Loguru
- Alertas si los collectors fallan
- Métricas de disponibilidad de la API

## Dependencias Principales (requirements.txt)

```
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlalchemy==2.0.25
alembic==1.13.1
psycopg2-binary==2.9.9
pydantic==2.5.3
pydantic-settings==2.1.0
python-dotenv==1.0.0
requests==2.31.0
beautifulsoup4==4.12.3
lxml==5.1.0
apscheduler==3.10.4
loguru==0.7.2
pytest==7.4.4
pytest-asyncio==0.23.3
httpx==0.26.0
```

## Implementaciones Detalladas

A continuación se detallan las 17 implementaciones individuales. Cada una incluye:
- **ID**: Número de implementación
- **Dependencias**: Tareas que deben completarse antes
- **Archivos**: Archivos a crear o modificar
- **Pasos**: Lista de acciones específicas
- **Criterios de Aceptación**: Cómo verificar que está completa

---

### [01] Setup Inicial
**Dependencias**: Ninguna
**Tipo**: 🔴 Secuencial
**Duración**: 30 minutos

**Descripción**: Configurar el entorno de desarrollo básico con Python y PostgreSQL.

**Archivos**:
- `requirements.txt` (crear)
- `.env.example` (crear)
- `.gitignore` (crear)

**Pasos**:
1. Instalar Python 3.11+ si no está instalado
2. Instalar PostgreSQL 14+ localmente o via Docker
3. Crear directorio del proyecto: `financial-rates-api/`
4. Crear entorno virtual: `python -m venv venv`
5. Activar entorno virtual
6. Crear archivo `.gitignore` con:
   - `venv/`, `__pycache__/`, `.env`, `*.pyc`, `.pytest_cache/`
7. Crear archivo `requirements.txt` vacío (se llenará en tareas siguientes)
8. Crear archivo `.env.example` con variables de template

**Criterios de Aceptación**:
- ✅ Python 3.11+ instalado y funcionando
- ✅ PostgreSQL corriendo (verificar con `psql --version`)
- ✅ Entorno virtual creado y activado
- ✅ Archivos base creados

---

### [02] Estructura del Proyecto
**Dependencias**: [01]
**Tipo**: 🔴 Secuencial
**Duración**: 20 minutos

**Descripción**: Crear la estructura de directorios y archivos `__init__.py` necesarios.

**Archivos a crear**:
```
app/
├── __init__.py
├── models/__init__.py
├── schemas/__init__.py
├── collectors/__init__.py
└── routers/__init__.py
tests/
├── __init__.py
├── unit/__init__.py
└── integration/__init__.py
alembic/
planes/
└── implementaciones/
```

**Pasos**:
1. Crear directorio `app/` con subdirectorios
2. Crear archivos `__init__.py` en cada directorio Python
3. Crear estructura de directorios `tests/`
4. Crear directorio `alembic/` (vacío por ahora)
5. Crear directorio `planes/implementaciones/`
6. Crear `README.md` básico con descripción del proyecto

**Criterios de Aceptación**:
- ✅ Estructura de directorios completa
- ✅ Todos los `__init__.py` creados
- ✅ README.md existe

---

### [03] Base de Datos - Schema
**Dependencias**: [02]
**Tipo**: 🔴 Secuencial
**Duración**: 30 minutos

**Descripción**: Crear base de datos PostgreSQL y schema SQL inicial (sin ORM aún).

**Archivos**:
- `database/schema.sql` (crear)
- `database/init.sql` (crear)

**Pasos**:
1. Crear base de datos: `createdb financial_rates`
2. Crear directorio `database/`
3. Crear `schema.sql` con definición de tablas:
   - Tabla `cetes`
   - Tabla `sofipos`
   - Tabla `sofipo_plazos`
   - Tabla `fondos_etfs`
   - Índices necesarios
4. Ejecutar schema: `psql -d financial_rates -f database/schema.sql`
5. Verificar tablas creadas: `psql -d financial_rates -c "\dt"`

**Criterios de Aceptación**:
- ✅ Base de datos `financial_rates` existe
- ✅ Todas las tablas creadas correctamente
- ✅ Índices aplicados
- ✅ Constraints funcionando

---

### [04] Configuración y Environment
**Dependencias**: [03]
**Tipo**: 🔴 Secuencial
**Duración**: 30 minutos

**Descripción**: Implementar sistema de configuración con variables de entorno.

**Archivos**:
- `app/config.py` (crear)
- `.env` (crear, no commitear)
- `.env.example` (actualizar)

**Pasos**:
1. Agregar a `requirements.txt`:
   ```
   python-dotenv==1.0.0
   pydantic-settings==2.1.0
   ```
2. Instalar dependencias: `pip install -r requirements.txt`
3. Crear `app/config.py` con clase Settings usando Pydantic:
   - `DATABASE_URL`
   - `BANXICO_API_KEY`
   - `ALPHA_VANTAGE_API_KEY`
   - `LOG_LEVEL`
   - `ENVIRONMENT` (dev/prod)
4. Crear archivo `.env` con valores de desarrollo
5. Actualizar `.env.example` con variables sin valores

**Criterios de Aceptación**:
- ✅ `app/config.py` funciona y carga variables
- ✅ Validación de Pydantic funcionando
- ✅ `.env` no está en git
- ✅ `.env.example` documentado

---

### [05] Modelos SQLAlchemy - CETES
**Dependencias**: [04]
**Tipo**: 🟢 Paralelo (con [06], [07])
**Duración**: 45 minutos

**Descripción**: Implementar modelo ORM para tabla CETES.

**Archivos**:
- `app/database.py` (crear)
- `app/models/cetes.py` (crear)
- `app/schemas/cetes.py` (crear)

**Pasos**:
1. Agregar a `requirements.txt`:
   ```
   sqlalchemy==2.0.25
   psycopg2-binary==2.9.9
   alembic==1.13.1
   ```
2. Instalar: `pip install -r requirements.txt`
3. Crear `app/database.py`:
   - Engine de SQLAlchemy
   - SessionLocal factory
   - Base declarativa
   - Función `get_db()` dependency
4. Crear `app/models/cetes.py`:
   - Clase `Cetes` con columnas
   - Relationships si aplica
5. Crear `app/schemas/cetes.py`:
   - `CetesBase`, `CetesCreate`, `CetesResponse` (Pydantic)
6. Inicializar Alembic: `alembic init alembic`
7. Configurar `alembic.ini` con DATABASE_URL
8. Crear primera migración: `alembic revision --autogenerate -m "add cetes table"`
9. Aplicar: `alembic upgrade head`

**Criterios de Aceptación**:
- ✅ Modelo `Cetes` funciona con SQLAlchemy
- ✅ Schemas Pydantic validando correctamente
- ✅ Alembic configurado
- ✅ Migración aplicada sin errores

---

### [06] Modelos SQLAlchemy - SOFIPOs
**Dependencias**: [04]
**Tipo**: 🟢 Paralelo (con [05], [07])
**Duración**: 45 minutos

**Descripción**: Implementar modelos ORM para tablas SOFIPOs.

**Archivos**:
- `app/models/sofipos.py` (crear)
- `app/schemas/sofipos.py` (crear)

**Pasos**:
1. Crear `app/models/sofipos.py`:
   - Clase `Sofipo`
   - Clase `SofipoPlazo`
   - Relationship entre ellas (one-to-many)
2. Crear `app/schemas/sofipos.py`:
   - `SofipoBase`, `SofipoCreate`, `SofipoResponse`
   - `SofipoPlazoBase`, `SofipoPlazoCreate`, `SofipoPlazoResponse`
   - `SofipoWithPlazos` (incluye plazos anidados)
3. Crear migración: `alembic revision --autogenerate -m "add sofipos tables"`
4. Aplicar: `alembic upgrade head`

**Criterios de Aceptación**:
- ✅ Modelos `Sofipo` y `SofipoPlazo` funcionan
- ✅ Relationship funciona correctamente
- ✅ Schemas Pydantic con nested data
- ✅ Migración aplicada

---

### [07] Modelos SQLAlchemy - Fondos/ETFs
**Dependencias**: [04]
**Tipo**: 🟢 Paralelo (con [05], [06])
**Duración**: 40 minutos

**Descripción**: Implementar modelo ORM para tabla fondos_etfs.

**Archivos**:
- `app/models/fondos.py` (crear)
- `app/schemas/fondos.py` (crear)

**Pasos**:
1. Crear `app/models/fondos.py`:
   - Clase `FondoETF`
2. Crear `app/schemas/fondos.py`:
   - `FondoBase`, `FondoCreate`, `FondoResponse`
   - Enum para tipos: `TipoFondo`, `Mercado`
3. Crear migración: `alembic revision --autogenerate -m "add fondos_etfs table"`
4. Aplicar: `alembic upgrade head`

**Criterios de Aceptación**:
- ✅ Modelo `FondoETF` funciona
- ✅ Schemas con enums validando tipos
- ✅ Migración aplicada

---

### [08] Collector Banxico - CETES
**Dependencias**: [05]
**Tipo**: 🟢 Paralelo (con [09], [10])
**Duración**: 2 horas

**Descripción**: Implementar recopilador de datos de CETES desde API de Banxico.

**Archivos**:
- `app/collectors/banxico_collector.py` (crear)
- `tests/unit/test_banxico_collector.py` (crear)

**Pasos**:
1. Registrarse en Banxico SIE: https://www.banxico.org.mx/SieAPIRest/service/v1/?locale=en
2. Obtener token y agregarlo a `.env` como `BANXICO_API_KEY`
3. Agregar a `requirements.txt`:
   ```
   requests==2.31.0
   loguru==0.7.2
   ```
4. Instalar: `pip install -r requirements.txt`
5. Crear `app/collectors/banxico_collector.py`:
   - Clase `BanxicoCollector`
   - Método `get_cetes_rate(serie_id)` para obtener una serie
   - Método `get_all_cetes()` para obtener todas las series
   - Método `save_to_db(session, data)` para guardar en DB
   - Manejo de errores HTTP
   - Logging con Loguru
6. Crear constantes para series:
   ```python
   CETES_SERIES = {
       28: "SF43936",
       91: "SF43939",
       182: "SF43942",
       364: "SF43945"
   }
   ```
7. Crear tests unitarios con mocks
8. Crear script ejecutable: `if __name__ == "__main__":`

**Criterios de Aceptación**:
- ✅ Puede obtener datos de API de Banxico
- ✅ Datos se guardan en tabla `cetes`
- ✅ Manejo de errores robusto
- ✅ Logs informativos
- ✅ Tests unitarios pasan

---

### [09] Scraper SOFIPOs
**Dependencias**: [06]
**Tipo**: 🟢 Paralelo (con [08], [10])
**Duración**: 3 horas

**Descripción**: Implementar web scraper para obtener rendimientos de SOFIPOs.

**Archivos**:
- `app/collectors/sofipo_scraper.py` (crear)
- `tests/unit/test_sofipo_scraper.py` (crear)

**Pasos**:
1. Agregar a `requirements.txt`:
   ```
   beautifulsoup4==4.12.3
   lxml==5.1.0
   ```
2. Instalar: `pip install -r requirements.txt`
3. Analizar estructura HTML de https://www.tasas.mx/
   - Inspeccionar tablas de SOFIPOs
   - Identificar selectores CSS
4. Crear `app/collectors/sofipo_scraper.py`:
   - Clase `SofipoScraper`
   - Método `fetch_html(url)` con User-Agent apropiado
   - Método `parse_sofipos(html)` para extraer datos
   - Método `parse_plazos(html, sofipo_id)` para plazos
   - Método `save_to_db(session, data)` para guardar
   - Rate limiting (sleep entre requests)
   - Logging
5. Implementar manejo de errores:
   - Timeout de requests
   - Parsing errors
   - Validation con Pydantic
6. Crear tests con HTML mock
7. Verificar `robots.txt` de Tasas.mx

**Criterios de Aceptación**:
- ✅ Puede scrapear datos de Tasas.mx
- ✅ Extrae SOFIPOs con sus GAT
- ✅ Extrae rendimientos por plazo
- ✅ Guarda correctamente en DB
- ✅ Respeta rate limiting
- ✅ Tests pasan

---

### [10] Collector ETFs
**Dependencias**: [07]
**Tipo**: 🟢 Paralelo (con [08], [09])
**Duración**: 2 horas

**Descripción**: Implementar collector para obtener datos de fondos/ETFs desde API externa.

**Archivos**:
- `app/collectors/etf_collector.py` (crear)
- `app/collectors/tickers.json` (crear - lista de tickers)
- `tests/unit/test_etf_collector.py` (crear)

**Pasos**:
1. Registrarse en Alpha Vantage: https://www.alphavantage.co/support/#api-key
2. Obtener API key y agregar a `.env` como `ALPHA_VANTAGE_API_KEY`
3. Crear `app/collectors/etf_collector.py`:
   - Clase `ETFCollector`
   - Método `get_etf_data(ticker)` para obtener datos de un ticker
   - Método `get_global_quote(ticker)` para precio actual
   - Método `calculate_performance(data)` para rendimientos
   - Método `save_to_db(session, data)`
   - Rate limiting (5 requests/min para tier gratuito)
   - Retry logic
   - Logging
4. Crear `app/collectors/tickers.json` con lista inicial:
   ```json
   {
     "etfs": [
       {"ticker": "SPY", "name": "SPDR S&P 500", "market": "US"},
       {"ticker": "QQQ", "name": "Invesco QQQ", "market": "US"},
       {"ticker": "VOO", "name": "Vanguard S&P 500", "market": "US"}
     ]
   }
   ```
5. Crear tests con respuestas mock de API
6. Script ejecutable

**Criterios de Aceptación**:
- ✅ Puede obtener datos de Alpha Vantage
- ✅ Calcula rendimientos correctamente
- ✅ Guarda en tabla `fondos_etfs`
- ✅ Respeta rate limits
- ✅ Tests pasan

---

### [11] Scheduler
**Dependencias**: [08], [09], [10]
**Tipo**: 🔴 Secuencial
**Duración**: 1.5 horas

**Descripción**: Implementar scheduler para ejecutar collectors automáticamente.

**Archivos**:
- `app/scheduler.py` (crear)
- `app/main.py` (crear - entry point)

**Pasos**:
1. Agregar a `requirements.txt`:
   ```
   apscheduler==3.10.4
   ```
2. Instalar: `pip install -r requirements.txt`
3. Crear `app/scheduler.py`:
   - Configurar APScheduler con BackgroundScheduler
   - Job para CETES: diario a las 11:00 AM
   - Job para SOFIPOs: diario a las 7:00 AM
   - Job para ETFs: diario a las 8:00 PM
   - Configurar logging de jobs
   - Error handlers
   - Función `start_scheduler()`
4. Crear `app/main.py` temporal:
   ```python
   from app.scheduler import start_scheduler

   if __name__ == "__main__":
       start_scheduler()
   ```
5. Configurar timezone (Mexico City: America/Mexico_City)
6. Agregar opción para ejecución manual/inmediata

**Criterios de Aceptación**:
- ✅ Scheduler inicia correctamente
- ✅ Jobs se ejecutan en horarios configurados
- ✅ Logs muestran ejecuciones
- ✅ Manejo de errores funciona

---

### [12] Router API - CETES
**Dependencias**: [11]
**Tipo**: 🟢 Paralelo (con [13], [14])
**Duración**: 1.5 horas

**Descripción**: Implementar endpoints REST para consultar datos de CETES.

**Archivos**:
- `app/routers/cetes.py` (crear)
- `app/main.py` (actualizar - crear app FastAPI)
- `tests/integration/test_cetes_api.py` (crear)

**Pasos**:
1. Agregar a `requirements.txt`:
   ```
   fastapi==0.109.0
   uvicorn[standard]==0.27.0
   httpx==0.26.0
   pytest==7.4.4
   pytest-asyncio==0.23.3
   ```
2. Instalar: `pip install -r requirements.txt`
3. Actualizar `app/main.py`:
   - Crear app FastAPI
   - Configurar CORS
   - Incluir router de CETES
   - Agregar endpoint raíz `/` con info de la API
4. Crear `app/routers/cetes.py`:
   - `GET /api/cetes` - Listar tasas actuales (últimas de cada plazo)
   - `GET /api/cetes/{plazo}` - Tasa actual de un plazo específico
   - `GET /api/cetes/historico` - Serie histórica (con query params: plazo, fecha_inicio, fecha_fin)
   - Dependency `get_db` inyectada
   - Responses con schemas Pydantic
5. Crear tests de integración con TestClient
6. Documentar con docstrings para OpenAPI

**Criterios de Aceptación**:
- ✅ FastAPI app corre: `uvicorn app.main:app --reload`
- ✅ Todos los endpoints responden correctamente
- ✅ Swagger docs accesibles en `/docs`
- ✅ Tests de integración pasan

---

### [13] Router API - SOFIPOs
**Dependencias**: [11]
**Tipo**: 🟢 Paralelo (con [12], [14])
**Duración**: 1.5 horas

**Descripción**: Implementar endpoints REST para consultar datos de SOFIPOs.

**Archivos**:
- `app/routers/sofipos.py` (crear)
- `app/main.py` (actualizar)
- `tests/integration/test_sofipos_api.py` (crear)

**Pasos**:
1. Crear `app/routers/sofipos.py`:
   - `GET /api/sofipos` - Listar todas las SOFIPOs (con paginación)
   - `GET /api/sofipos/{sofipo_id}` - Detalle de SOFIPO con todos sus plazos
   - `GET /api/sofipos/top` - Top 10 SOFIPOs por GAT nominal
   - Query params: `limit`, `offset`, `ordenar_por` (gat_nominal, gat_real)
   - Response incluye plazos nested usando `SofipoWithPlazos`
2. Actualizar `app/main.py` para incluir router
3. Implementar paginación
4. Crear tests de integración

**Criterios de Aceptación**:
- ✅ Endpoints funcionan correctamente
- ✅ Paginación funciona
- ✅ Nested data (plazos) se retorna correctamente
- ✅ Tests pasan

---

### [14] Router API - Fondos/ETFs
**Dependencias**: [11]
**Tipo**: 🟢 Paralelo (con [12], [13])
**Duración**: 1.5 horas

**Descripción**: Implementar endpoints REST para consultar datos de fondos/ETFs.

**Archivos**:
- `app/routers/fondos.py` (crear)
- `app/main.py` (actualizar)
- `tests/integration/test_fondos_api.py` (crear)

**Pasos**:
1. Crear `app/routers/fondos.py`:
   - `GET /api/fondos` - Listar fondos (con filtros)
   - `GET /api/fondos/{ticker}` - Detalle de un fondo específico
   - `GET /api/fondos/buscar` - Búsqueda por nombre o ticker (query param: `q`)
   - Query params: `tipo`, `mercado`, `limit`, `offset`
   - Ordenamiento por rendimiento
2. Actualizar `app/main.py` para incluir router
3. Implementar búsqueda con SQL LIKE/ILIKE
4. Crear tests de integración

**Criterios de Aceptación**:
- ✅ Endpoints funcionan
- ✅ Filtros por tipo y mercado funcionan
- ✅ Búsqueda funciona correctamente
- ✅ Tests pasan

---

### [15] Router API - Comparación
**Dependencias**: [12], [13], [14]
**Tipo**: 🔴 Secuencial
**Duración**: 2 horas

**Descripción**: Implementar endpoint para comparar rendimientos entre CETES, SOFIPOs y Fondos.

**Archivos**:
- `app/routers/comparar.py` (crear)
- `app/schemas/comparar.py` (crear)
- `app/main.py` (actualizar)
- `tests/integration/test_comparar_api.py` (crear)

**Pasos**:
1. Crear `app/schemas/comparar.py`:
   - `ComparacionResponse` con campos:
     - `cetes`: lista de tasas actuales
     - `sofipos_top`: top 5 SOFIPOs
     - `fondos_top`: top 5 fondos
     - `mejor_opcion`: análisis del mejor rendimiento
2. Crear `app/routers/comparar.py`:
   - `GET /api/comparar` - Comparación general
   - `GET /api/comparar/plazo/{dias}` - Comparar por plazo similar
   - Lógica para determinar mejor opción considerando:
     - Liquidez
     - Rendimiento
     - Riesgo (CETES < SOFIPOs < Fondos)
3. Implementar queries complejas
4. Actualizar `app/main.py`
5. Crear tests

**Criterios de Aceptación**:
- ✅ Endpoint retorna comparación completa
- ✅ Lógica de "mejor opción" funciona
- ✅ Response bien estructurado
- ✅ Tests pasan

---

### [16] Tests & Documentación
**Dependencias**: [12], [13], [14], [15]
**Tipo**: 🟢 Paralelo (con [17])
**Duración**: 3 horas

**Descripción**: Completar suite de tests y documentación del proyecto.

**Archivos**:
- `tests/` (completar todos los tests)
- `README.md` (actualizar)
- `docs/API.md` (crear)
- `docs/SETUP.md` (crear)

**Pasos**:
1. Completar tests unitarios faltantes:
   - Cobertura >80%
   - Tests para edge cases
   - Tests para manejo de errores
2. Agregar tests de integración end-to-end:
   - Test completo: collect -> store -> retrieve
3. Configurar pytest coverage:
   ```bash
   pytest --cov=app --cov-report=html tests/
   ```
4. Actualizar `README.md` con:
   - Descripción del proyecto
   - Características principales
   - Stack tecnológico
   - Instrucciones de instalación
   - Cómo obtener API keys
   - Comandos para correr
5. Crear `docs/API.md`:
   - Documentar todos los endpoints
   - Ejemplos de requests/responses
   - Códigos de error
6. Crear `docs/SETUP.md`:
   - Setup detallado paso a paso
   - Troubleshooting común

**Criterios de Aceptación**:
- ✅ Cobertura de tests >80%
- ✅ Todos los tests pasan
- ✅ README completo y claro
- ✅ Documentación de API detallada

---

### [17] Docker & Deployment
**Dependencias**: [12], [13], [14], [15]
**Tipo**: 🟢 Paralelo (con [16])
**Duración**: 2 horas

**Descripción**: Containerizar aplicación y preparar para deployment.

**Archivos**:
- `Dockerfile` (crear)
- `docker-compose.yml` (crear)
- `.dockerignore` (crear)
- `docs/DEPLOYMENT.md` (crear)

**Pasos**:
1. Crear `Dockerfile`:
   - FROM python:3.11-slim
   - Instalar dependencias
   - Copiar código
   - Exponer puerto 8000
   - CMD con uvicorn
2. Crear `docker-compose.yml`:
   - Service: postgres (con volume)
   - Service: api (build from Dockerfile)
   - Network
   - Variables de entorno
   - Health checks
3. Crear `.dockerignore`:
   - venv/, __pycache__/, .git/, etc.
4. Probar build:
   ```bash
   docker-compose build
   docker-compose up -d
   ```
5. Verificar que funciona:
   ```bash
   curl http://localhost:8000/api/cetes
   ```
6. Crear `docs/DEPLOYMENT.md`:
   - Instrucciones de deployment con Docker
   - Variables de entorno de producción
   - Consideraciones de seguridad

**Criterios de Aceptación**:
- ✅ Docker build exitoso
- ✅ docker-compose up funciona
- ✅ Aplicación accesible en container
- ✅ Base de datos persiste con volumes
- ✅ Documentación de deployment completa

---

## Próximos Pasos Después de Aprobación del Plan

### Acciones Inmediatas
1. **Salir de plan mode** y crear estructura de proyecto:
   ```
   financial-rates-api/
   └── planes/
       ├── plan-completo.md (este archivo)
       └── implementaciones/
           ├── LEEME.md (índice y guía)
           ├── 01-setup-inicial.md
           ├── 02-estructura-proyecto.md
           ├── ...
           └── 17-docker-deploy.md
   ```

2. **Generar archivos individuales** de implementación:
   - Cada archivo en `implementaciones/` contendrá el detalle de una tarea
   - Formato consistente para fácil referencia
   - Links cruzados entre dependencias

3. **Crear LEEME.md** en `implementaciones/` con:
   - Índice de todas las implementaciones
   - Grafo visual de dependencias
   - Guía de cómo usar los archivos

### Flujo de Trabajo Sugerido
1. Leer `plan-completo.md` para contexto general
2. Ir a `implementaciones/LEEME.md` para ver el índice
3. Comenzar con implementación [01]
4. Marcar como completadas en el LEEME
5. Seguir el grafo de dependencias
6. Aprovechar paralelización cuando sea posible

### Obtener API Keys
- **Banxico**: https://www.banxico.org.mx/SieAPIRest/service/v1/?locale=en (gratuito)
- **Alpha Vantage**: https://www.alphavantage.co/support/#api-key (gratuito con limitaciones)

### Iniciar Implementación
Una vez aprobado el plan y con la estructura creada:
```bash
cd financial-rates-api
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
# Seguir implementación [01] en planes/implementaciones/01-setup-inicial.md
```
