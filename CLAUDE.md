# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Financial Rates API** is a Python system that collects daily financial returns from Mexican CETES, SOFIPOs, and international investment funds/ETFs, stores them in PostgreSQL, and exposes a REST API for querying.

**Current Status**: Planning phase complete. Implementation follows 17 modular tasks in `planes/implementaciones/`.

## Architecture

### Data Flow
```
External APIs/Scraping → Collectors → PostgreSQL → FastAPI REST API
```

**Three data collection pipelines:**
1. **CETES**: Banxico SIE API → `app/collectors/banxico_collector.py` → `cetes` table
2. **SOFIPOs**: Web scraping (Tasas.mx) → `app/collectors/sofipo_scraper.py` → `sofipos` + `sofipo_plazos` tables
3. **ETFs**: Alpha Vantage API → `app/collectors/etf_collector.py` → `fondos_etfs` table

**Scheduler**: APScheduler runs collectors daily at configured times (see `app/scheduler.py`)

### Key Components

- **Models** (`app/models/`): SQLAlchemy 2.0 ORM models for database tables
  - `cetes.py`: CETES rates by term (28, 91, 182, 364 days)
  - `sofipos.py`: SOFIPO institutions + their term rates (one-to-many relationship)
  - `fondos.py`: International funds/ETFs with market/type classification

- **Schemas** (`app/schemas/`): Pydantic validation schemas matching models
  - Include nested schemas (e.g., `SofipoWithPlazos` embeds term rates)
  - Use enums for `TipoFondo` and `Mercado` in fondos

- **Collectors** (`app/collectors/`): Data acquisition modules
  - Each collector has: `collect()` method, `save_to_db()`, error handling, logging
  - Rate limiting implemented for external APIs
  - Duplicate prevention via unique constraints

- **Routers** (`app/routers/`): FastAPI endpoint groups
  - `cetes.py`: Current rates, historical series
  - `sofipos.py`: List with pagination, detail with nested terms
  - `fondos.py`: Filters by type/market, search functionality
  - `comparar.py`: Cross-instrument comparison endpoint

- **Database** (`app/database.py`): SQLAlchemy engine, session factory, `get_db()` dependency

- **Config** (`app/config.py`): Pydantic Settings for environment variables

## Database Schema

**Tables:**
- `cetes`: (id, plazo, tasa, fecha_subasta, fecha_vencimiento, created_at)
  - Unique constraint on (plazo, fecha_subasta)
- `sofipos`: (id, nombre, gat_nominal, gat_real, fecha_actualizacion, created_at)
- `sofipo_plazos`: (id, sofipo_id, plazo, tasa, fecha_actualizacion, created_at)
  - Foreign key to sofipos with CASCADE delete
- `fondos_etfs`: (id, ticker, nombre, tipo, mercado, precio_actual, rendimiento_anual, rendimiento_ytd, fecha_actualizacion, created_at)
  - Unique constraint on (ticker, fecha_actualizacion)

**Migrations**: Managed by Alembic in `alembic/versions/`

## Development Commands

### Setup (First Time)
```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Create database
createdb financial_rates
# Or with Docker: docker run --name postgres-financial -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:14

# Apply database schema
psql -U postgres -d financial_rates -f database/schema.sql

# Configure environment
cp .env.example .env
# Edit .env with your API keys
```

### Database Migrations
```bash
# Create migration after model changes
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1

# View migration history
alembic history --verbose
```

### Running Collectors
```bash
# Run individual collectors
python -m app.collectors.banxico_collector
python -m app.collectors.sofipo_scraper
python -m app.collectors.etf_collector

# Verify data
psql -U postgres -d financial_rates -c "SELECT * FROM cetes LIMIT 5;"
psql -U postgres -d financial_rates -c "SELECT * FROM sofipos LIMIT 5;"
```

### Running the API
```bash
# Development server with auto-reload
uvicorn app.main:app --reload

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Access documentation
# http://localhost:8000/docs (Swagger UI)
# http://localhost:8000/redoc (ReDoc)
```

### Running Scheduler
```bash
# Start scheduler (runs collectors at configured times)
python app/main.py
# Check logs: tail -f logs/scheduler.log
```

### Testing
```bash
# Run all tests
pytest

# Unit tests only
pytest tests/unit/ -v

# Integration tests only
pytest tests/integration/ -v

# Single test file
pytest tests/unit/test_banxico_collector.py -v

# With coverage
pytest --cov=app --cov-report=html tests/
# View: open htmlcov/index.html
```

### Docker
```bash
# Build and run with docker-compose
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop containers
docker-compose down

# Rebuild after changes
docker-compose up -d --build
```

## Implementation Guide

**The project is organized into 17 sequential/parallel tasks.** See `planes/implementaciones/LEEME.md` for the complete dependency graph and task index.

### Task Dependencies (7 Levels):
- **Level 1** (01-04): Foundation - must be done sequentially
- **Level 2** (05-07): Models - can be done in parallel
- **Level 3** (08-10): Collectors - can be done in parallel
- **Level 4** (11): Scheduler - requires all collectors
- **Level 5** (12-14): API routers - can be done in parallel
- **Level 6** (15): Comparison router - requires other routers
- **Level 7** (16-17): Tests and Docker - can be done in parallel

**To start implementing:**
1. Read `planes/plan-completo.md` for full context
2. Follow tasks in order starting with `planes/implementaciones/01-setup-inicial.md`
3. Each task file contains: dependencies, steps, acceptance criteria, verification commands

## External APIs

**Banxico SIE (CETES data):**
- Register: https://www.banxico.org.mx/SieAPIRest/service/v1/?locale=en
- Free token sent by email
- Series IDs: SF43936 (28d), SF43939 (91d), SF43942 (182d), SF43945 (364d)
- Add to `.env`: `BANXICO_API_KEY=your_token`

**Alpha Vantage (ETF/Fund data):**
- Register: https://www.alphavantage.co/support/#api-key
- Free tier: 25 requests/day
- Add to `.env`: `ALPHA_VANTAGE_API_KEY=your_key`

**Tasas.mx (SOFIPOs):**
- No API - web scraping required
- Check `robots.txt` before scraping
- Implement rate limiting (1-2 seconds between requests)

## Key Patterns

**Collector Pattern:**
```python
class Collector:
    def __init__(self, api_key=None):
        # Initialize with config

    def collect(self) -> int:
        # Main entry point, returns count saved
        data = self.fetch_data()
        return self.save_to_db(data)

    def save_to_db(self, data):
        # Check for duplicates via unique constraints
        # Use try/except with rollback
```

**Router Pattern:**
```python
router = APIRouter()

@router.get("/endpoint")
def endpoint(db: Session = Depends(get_db)):
    # Use ORM queries
    # Return Pydantic schema
    # Handle pagination with limit/offset
```

**Alembic env.py Setup:**
```python
# Import all models for autogenerate
from app.models.cetes import Cetes
from app.models.sofipos import Sofipo, SofipoPlazo
from app.models.fondos import FondoETF

# Set target metadata
target_metadata = Base.metadata

# Use config from app
config.set_main_option("sqlalchemy.url", get_database_url())
```

## Configuration

**Environment Variables** (`.env`):
- `DATABASE_URL`: PostgreSQL connection string
- `BANXICO_API_KEY`: Token from Banxico SIE
- `ALPHA_VANTAGE_API_KEY`: API key from Alpha Vantage
- `ENVIRONMENT`: development/production
- `LOG_LEVEL`: DEBUG/INFO/WARNING/ERROR
- `ENABLE_SCHEDULER`: true/false

**Managed by** `app/config.py` using Pydantic Settings with validation.

## Important Notes

- **SQLAlchemy 2.0**: Uses new API (not legacy `query()` style)
- **Pydantic v2**: Use `model_validate()`, `model_dump()`, `ConfigDict`
- **Timezone**: Scheduler uses `America/Mexico_City`
- **Unique Constraints**: Prevent duplicate data in all tables
- **Relationships**: `Sofipo.plazos` is one-to-many with cascade delete
- **Logging**: Use `loguru` for all collectors and scheduler
- **Rate Limiting**: Implement in all external API calls
- **Error Handling**: All collectors must handle HTTP errors, parsing errors, DB errors

## Verification Queries

```sql
-- Check CETES data
SELECT plazo, tasa, fecha_subasta FROM cetes
ORDER BY fecha_subasta DESC LIMIT 10;

-- Check SOFIPOs with nested plazos
SELECT s.nombre, s.gat_nominal, sp.plazo, sp.tasa
FROM sofipos s
JOIN sofipo_plazos sp ON s.id = sp.sofipo_id
ORDER BY s.gat_nominal DESC;

-- Check ETFs/Funds
SELECT ticker, tipo, mercado, rendimiento_anual
FROM fondos_etfs
ORDER BY rendimiento_anual DESC LIMIT 10;

-- Migration status
SELECT * FROM alembic_version;
```
