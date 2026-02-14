"""
Financial Rates API - Aplicación Principal

API REST para consultar rendimientos financieros de:
- CETES (Certificados de la Tesorería)
- SOFIPOs (Sociedades Financieras Populares)
- ETFs y Fondos de Inversión
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_pool, close_pool
from app.routers import cetes, sofipos, fondos, comparar


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Maneja el ciclo de vida de la aplicación."""
    # Startup
    init_pool()
    yield
    # Shutdown
    close_pool()


app = FastAPI(
    title="Financial Rates API",
    description="""
API para consultar rendimientos financieros en México.

## Endpoints disponibles

- **CETES**: Tasas de Certificados de la Tesorería
- **SOFIPOs**: Rendimientos de Sociedades Financieras Populares
- **Fondos/ETFs**: Precios y rendimientos de ETFs internacionales
- **Comparar**: Comparación entre diferentes instrumentos

## Fuentes de datos

- CETES: API oficial de Banxico SIE
- SOFIPOs: Datos públicos de instituciones reguladas
- ETFs: Alpha Vantage API
    """,
    version="1.0.0",
    lifespan=lifespan,
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(cetes.router, prefix="/api")
app.include_router(sofipos.router, prefix="/api")
app.include_router(fondos.router, prefix="/api")
app.include_router(comparar.router, prefix="/api")


@app.get("/")
def root():
    """Información de la API."""
    return {
        "nombre": "Financial Rates API",
        "version": "1.0.0",
        "descripcion": "API para consultar rendimientos financieros en México",
        "endpoints": {
            "cetes": "/api/cetes",
            "sofipos": "/api/sofipos",
            "fondos": "/api/fondos",
            "comparar": "/api/comparar",
        },
        "documentacion": "/docs",
    }


@app.get("/health")
def health_check():
    """Health check para monitoreo."""
    return {"status": "ok", "environment": settings.ENVIRONMENT}
