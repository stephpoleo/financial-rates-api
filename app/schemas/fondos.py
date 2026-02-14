"""Schemas Pydantic para Fondos/ETFs."""

from datetime import date
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field, ConfigDict


class TipoFondo(str, Enum):
    """Tipos de fondos."""
    ETF = "ETF"
    MUTUAL_FUND = "MUTUAL_FUND"
    INDEX_FUND = "INDEX_FUND"


class Mercado(str, Enum):
    """Mercados disponibles."""
    US = "US"
    MX = "MX"
    EU = "EU"
    GLOBAL = "GLOBAL"


class FondoBase(BaseModel):
    """Schema base de Fondo/ETF."""
    ticker: str = Field(..., max_length=20)
    nombre: str | None = Field(None, max_length=200)
    tipo: str | None = None
    mercado: str | None = None
    precio_actual: Decimal | None = None
    rendimiento_anual: Decimal | None = None
    rendimiento_ytd: Decimal | None = None
    fecha_actualizacion: date


class FondoCreate(FondoBase):
    """Schema para crear Fondo/ETF."""
    pass


class FondoResponse(FondoBase):
    """Schema de respuesta de Fondo/ETF."""
    id: int

    model_config = ConfigDict(from_attributes=True)
