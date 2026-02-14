"""Schemas Pydantic para SOFIPOs."""

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict


class SofipoPlazoBase(BaseModel):
    """Schema base para plazo de SOFIPO."""
    plazo: int = Field(..., description="Plazo en días")
    tasa: Decimal = Field(..., description="Tasa de rendimiento")
    fecha_actualizacion: date


class SofipoPlazoCreate(SofipoPlazoBase):
    """Schema para crear plazo de SOFIPO."""
    sofipo_id: int


class SofipoPlazoResponse(SofipoPlazoBase):
    """Schema de respuesta para plazo."""
    id: int

    model_config = ConfigDict(from_attributes=True)


class SofipoBase(BaseModel):
    """Schema base de SOFIPO."""
    nombre: str = Field(..., max_length=200)
    gat_nominal: Decimal | None = Field(None, description="GAT Nominal")
    gat_real: Decimal | None = Field(None, description="GAT Real")
    fecha_actualizacion: date


class SofipoCreate(SofipoBase):
    """Schema para crear SOFIPO."""
    pass


class SofipoResponse(SofipoBase):
    """Schema de respuesta de SOFIPO."""
    id: int

    model_config = ConfigDict(from_attributes=True)


class SofipoWithPlazos(SofipoResponse):
    """SOFIPO con sus plazos incluidos."""
    plazos: list[SofipoPlazoResponse] = []
