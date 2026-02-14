# [12] Router API - CETES

**Estado**: ⬜ Pendiente | **Dependencias**: [11] | **Tipo**: 🟢 Paralelo | **Duración**: 1.5 horas

## Descripción
Implementar endpoints REST de FastAPI para consultar datos de CETES.

## Archivos
- `app/routers/cetes.py`
- `app/main.py` (crear/actualizar)
- `tests/integration/test_cetes_api.py`

## Dependencias
```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
httpx==0.26.0
pytest==7.4.4
pytest-asyncio==0.23.3
```

## Endpoints
- `GET /api/cetes` - Tasas actuales (últimas de cada plazo)
- `GET /api/cetes/{plazo}` - Tasa actual de plazo específico
- `GET /api/cetes/historico?plazo=28&fecha_inicio=2026-01-01` - Serie histórica

## app/main.py
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import cetes
from app.config import settings

app = FastAPI(
    title="Financial Rates API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(cetes.router, prefix="/api", tags=["CETES"])

@app.get("/")
def root():
    return {"message": "Financial Rates API", "docs": "/docs"}
```

## Criterios de Aceptación
- [ ] FastAPI app corre: `uvicorn app.main:app --reload`
- [ ] Endpoints responden correctamente
- [ ] Swagger docs en `/docs` funcionan
- [ ] Tests de integración pasan: `pytest tests/integration/`

## Verificación
```bash
uvicorn app.main:app --reload
curl http://localhost:8000/api/cetes
curl http://localhost:8000/api/cetes/28
```

➡️ **Próxima**: [13] Router API - SOFIPOs (paralelo)
