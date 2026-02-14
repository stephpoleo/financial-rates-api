# [07] Modelos SQLAlchemy - Fondos/ETFs

**Estado**: ⬜ Pendiente
**Dependencias**: [04] Configuración y Environment
**Tipo**: 🟢 Paralelo (con [05], [06])
**Duración estimada**: 40 minutos

## Descripción
Implementar modelo ORM para la tabla fondos_etfs y crear schemas Pydantic con enums para tipos y mercados.

## Prerequisitos
- Tarea [04] completada
- `app/database.py` existe

## Archivos a crear
- `app/models/fondos.py` (crear)
- `app/schemas/fondos.py` (crear)

## Pasos de implementación

### 1. Crear `app/models/fondos.py`

```python
# Archivo: app/models/fondos.py
"""
Modelo ORM para tabla fondos_etfs.
"""

from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime
from sqlalchemy.sql import func
from app.database import Base


class FondoETF(Base):
    """Modelo para fondos de inversión y ETFs."""

    __tablename__ = "fondos_etfs"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(20), nullable=False, index=True)
    nombre = Column(String(200), nullable=True)
    tipo = Column(String(50), nullable=True)  # 'ETF', 'MUTUAL_FUND', etc.
    mercado = Column(String(50), nullable=True)  # 'US', 'MX', 'EU', etc.
    precio_actual = Column(Numeric(10, 2), nullable=True)
    rendimiento_anual = Column(Numeric(5, 2), nullable=True)
    rendimiento_ytd = Column(Numeric(5, 2), nullable=True)
    fecha_actualizacion = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<FondoETF(ticker={self.ticker}, tipo={self.tipo}, mercado={self.mercado})>"
```

### 2. Crear `app/schemas/fondos.py`

```python
# Archivo: app/schemas/fondos.py
"""
Schemas Pydantic para validación de datos de fondos y ETFs.
"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import date
from decimal import Decimal
from typing import Optional
from enum import Enum


class TipoFondo(str, Enum):
    """Enum para tipos de fondos."""
    ETF = "ETF"
    MUTUAL_FUND = "MUTUAL_FUND"
    INDEX_FUND = "INDEX_FUND"
    BOND_FUND = "BOND_FUND"
    MONEY_MARKET = "MONEY_MARKET"
    OTHER = "OTHER"


class Mercado(str, Enum):
    """Enum para mercados."""
    US = "US"
    MX = "MX"
    EU = "EU"
    ASIA = "ASIA"
    LATAM = "LATAM"
    GLOBAL = "GLOBAL"
    OTHER = "OTHER"


class FondoBase(BaseModel):
    """Schema base para fondos/ETFs."""
    ticker: str = Field(..., description="Ticker del fondo/ETF", max_length=20)
    nombre: Optional[str] = Field(None, description="Nombre completo")
    tipo: Optional[TipoFondo] = Field(None, description="Tipo de fondo")
    mercado: Optional[Mercado] = Field(None, description="Mercado principal")
    precio_actual: Optional[Decimal] = Field(None, description="Precio actual")
    rendimiento_anual: Optional[Decimal] = Field(None, description="Rendimiento anual %")
    rendimiento_ytd: Optional[Decimal] = Field(None, description="Rendimiento YTD %")
    fecha_actualizacion: date = Field(..., description="Fecha de actualización")


class FondoCreate(FondoBase):
    """Schema para crear un fondo/ETF."""
    pass


class FondoResponse(FondoBase):
    """Schema para respuesta de API."""
    id: int

    model_config = ConfigDict(from_attributes=True)


class FondoSearch(BaseModel):
    """Schema para búsqueda de fondos."""
    query: str = Field(..., description="Texto a buscar (ticker o nombre)")
    tipo: Optional[TipoFondo] = None
    mercado: Optional[Mercado] = None


class FondoComparison(BaseModel):
    """Schema para comparación de fondos."""
    ranking: int
    fondo: FondoResponse
    rendimiento_vs_sp500: Optional[Decimal] = None
    rendimiento_vs_cetes: Optional[Decimal] = None


class FondoStats(BaseModel):
    """Schema para estadísticas de fondos."""
    total_fondos: int
    por_tipo: dict[str, int]
    por_mercado: dict[str, int]
    mejor_rendimiento: Optional[FondoResponse] = None
    peor_rendimiento: Optional[FondoResponse] = None
```

### 3. Actualizar `app/models/__init__.py`

```python
# Archivo: app/models/__init__.py
"""
Importar todos los modelos para que Alembic los detecte.
"""

from app.models.cetes import Cetes
from app.models.sofipos import Sofipo, SofipoPlazo
from app.models.fondos import FondoETF

__all__ = ["Cetes", "Sofipo", "SofipoPlazo", "FondoETF"]
```

### 4. Crear migración
```bash
alembic revision --autogenerate -m "add fondos_etfs table"
```

### 5. Aplicar migración
```bash
alembic upgrade head
```

### 6. Verificar en PostgreSQL
```bash
psql -U postgres -d financial_rates -c "\d fondos_etfs"
```

## Criterios de Aceptación

- [ ] Modelo `FondoETF` funciona
  ```python
  from app.models.fondos import FondoETF
  print(FondoETF.__tablename__)  # "fondos_etfs"
  ```

- [ ] Schemas con enums validando tipos
  ```python
  from app.schemas.fondos import FondoCreate, TipoFondo, Mercado

  # Debe aceptar valores del enum
  fondo = FondoCreate(
      ticker="SPY",
      tipo=TipoFondo.ETF,
      mercado=Mercado.US,
      fecha_actualizacion=date.today()
  )
  print(fondo.tipo)  # TipoFondo.ETF
  ```

- [ ] Migración aplicada
  ```bash
  alembic current
  ```

## Script de prueba

```python
# Archivo: test_fondos_model.py (temporal)
from datetime import date
from app.database import SessionLocal
from app.models.fondos import FondoETF

db = SessionLocal()

# Crear algunos ETFs de prueba
etfs_data = [
    {
        "ticker": "SPY",
        "nombre": "SPDR S&P 500 ETF",
        "tipo": "ETF",
        "mercado": "US",
        "precio_actual": 502.35,
        "rendimiento_anual": 12.5,
        "rendimiento_ytd": 2.1
    },
    {
        "ticker": "QQQ",
        "nombre": "Invesco QQQ Trust",
        "tipo": "ETF",
        "mercado": "US",
        "precio_actual": 472.18,
        "rendimiento_anual": 15.3,
        "rendimiento_ytd": 3.2
    },
    {
        "ticker": "CETETRC",
        "nombre": "CETES Trac",
        "tipo": "ETF",
        "mercado": "MX",
        "precio_actual": 106.50,
        "rendimiento_anual": 7.2,
        "rendimiento_ytd": 1.1
    }
]

for etf_data in etfs_data:
    etf = FondoETF(
        ticker=etf_data["ticker"],
        nombre=etf_data["nombre"],
        tipo=etf_data["tipo"],
        mercado=etf_data["mercado"],
        precio_actual=etf_data["precio_actual"],
        rendimiento_anual=etf_data["rendimiento_anual"],
        rendimiento_ytd=etf_data["rendimiento_ytd"],
        fecha_actualizacion=date.today()
    )
    db.add(etf)

db.commit()

# Consultar
fondos = db.query(FondoETF).all()
print(f"✓ {len(fondos)} fondos/ETFs creados")

# Consultar por mercado
fondos_us = db.query(FondoETF).filter(FondoETF.mercado == "US").all()
print(f"✓ Fondos US: {len(fondos_us)}")

# Ordenar por rendimiento
top_fondos = db.query(FondoETF).order_by(
    FondoETF.rendimiento_anual.desc()
).limit(3).all()

print("\n✓ Top 3 por rendimiento:")
for i, f in enumerate(top_fondos, 1):
    print(f"  {i}. {f.ticker}: {f.rendimiento_anual}%")

db.close()
```

## Test de enums

```python
# Test de enums
from app.schemas.fondos import FondoCreate, TipoFondo, Mercado
from datetime import date

# Válido - usando enum
fondo1 = FondoCreate(
    ticker="VOO",
    tipo=TipoFondo.ETF,
    mercado=Mercado.US,
    fecha_actualizacion=date.today()
)
print(f"✓ Tipo: {fondo1.tipo.value}")

# Válido - usando string (se convierte a enum)
fondo2 = FondoCreate(
    ticker="QQQ",
    tipo="ETF",
    mercado="US",
    fecha_actualizacion=date.today()
)
print(f"✓ Tipo: {fondo2.tipo.value}")

# Inválido - debe fallar
try:
    fondo3 = FondoCreate(
        ticker="XXX",
        tipo="INVALID_TYPE",  # No existe en enum
        mercado="US",
        fecha_actualizacion=date.today()
    )
except ValueError as e:
    print(f"✓ Validación funciona: {e}")
```

## Notas adicionales

- Los enums mejoran la validación y previenen errores tipográficos
- `str, Enum` permite usar tanto el enum como string en JSON
- `UNIQUE(ticker, fecha_actualizacion)` permite histórico de precios
- Los rendimientos son opcionales (`Optional`) porque pueden no estar disponibles

## Troubleshooting

**Error en enum al consultar DB**
- Los enums son solo para Pydantic, la DB almacena strings
- Al convertir ORM → Pydantic, se valida automáticamente

**Error: "value is not a valid enumeration member"**
- El valor en la DB no coincide con ningún enum
- Usar `TipoFondo.OTHER` como fallback

## Próximas tareas
➡️ [08] Collector Banxico - CETES (requiere [05])
➡️ [09] Scraper SOFIPOs (requiere [06])
➡️ [10] Collector ETFs (requiere [07])
