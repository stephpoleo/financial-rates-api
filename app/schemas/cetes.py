"""Schemas Pydantic para CETES."""

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict


class CetesBase(BaseModel):
    """Schema base de CETES."""
    plazo: int = Field(..., description="Plazo en días (28, 91, 182, 364)")
    tasa: Decimal = Field(..., description="Tasa de rendimiento")
    fecha_subasta: date = Field(..., description="Fecha de subasta")
    fecha_vencimiento: date | None = Field(None, description="Fecha de vencimiento")


class CetesCreate(CetesBase):
    """Schema para crear un registro de CETES."""
    pass


class CetesResponse(CetesBase):
    """Schema para respuesta de API."""
    id: int

    model_config = ConfigDict(from_attributes=True)
