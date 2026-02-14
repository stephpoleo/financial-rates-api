# [06] Modelos SQLAlchemy - SOFIPOs

**Estado**: ⬜ Pendiente
**Dependencias**: [04] Configuración y Environment
**Tipo**: 🟢 Paralelo (con [05], [07])
**Duración estimada**: 45 minutos

## Descripción
Implementar modelos ORM para las tablas de SOFIPOs (sofip os y sofipo_plazos) con relationship one-to-many, y crear schemas Pydantic con nested data.

## Prerequisitos
- Tarea [04] completada
- `app/database.py` existe (de tarea [05] si se hace en paralelo, o crear versión básica)

## Archivos a crear
- `app/models/sofipos.py` (crear)
- `app/schemas/sofipos.py` (crear)

## Pasos de implementación

### 1. Crear `app/models/sofipos.py`

```python
# Archivo: app/models/sofipos.py
"""
Modelos ORM para tablas de SOFIPOs.
"""

from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Sofipo(Base):
    """Modelo para SOFIPOs (información general)."""

    __tablename__ = "sofipos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    gat_nominal = Column(Numeric(5, 2), nullable=True)
    gat_real = Column(Numeric(5, 2), nullable=True)
    fecha_actualizacion = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship one-to-many con plazos
    plazos = relationship(
        "SofipoPlazo",
        back_populates="sofipo",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Sofipo(nombre={self.nombre}, gat_nominal={self.gat_nominal})>"


class SofipoPlazo(Base):
    """Modelo para rendimientos por plazo de SOFIPOs."""

    __tablename__ = "sofipo_plazos"

    id = Column(Integer, primary_key=True, index=True)
    sofipo_id = Column(Integer, ForeignKey("sofipos.id", ondelete="CASCADE"), nullable=False)
    plazo = Column(Integer, nullable=False)  # días
    tasa = Column(Numeric(5, 2), nullable=False)
    fecha_actualizacion = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship back to Sofipo
    sofipo = relationship("Sofipo", back_populates="plazos")

    def __repr__(self):
        return f"<SofipoPlazo(sofipo_id={self.sofipo_id}, plazo={self.plazo}, tasa={self.tasa})>"
```

### 2. Crear `app/schemas/sofipos.py`

```python
# Archivo: app/schemas/sofipos.py
"""
Schemas Pydantic para validación de datos de SOFIPOs.
"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import date
from decimal import Decimal
from typing import Optional


# --- Schemas para SofipoPlazo ---

class SofipoPlazoBase(BaseModel):
    """Schema base para plazo de SOFIPO."""
    plazo: int = Field(..., description="Plazo en días")
    tasa: Decimal = Field(..., description="Tasa de rendimiento")
    fecha_actualizacion: date = Field(..., description="Fecha de actualización")


class SofipoPlazoCreate(SofipoPlazoBase):
    """Schema para crear un plazo de SOFIPO."""
    sofipo_id: int


class SofipoPlazoResponse(SofipoPlazoBase):
    """Schema para respuesta de API."""
    id: int
    sofipo_id: int

    model_config = ConfigDict(from_attributes=True)


# --- Schemas para Sofipo ---

class SofipoBase(BaseModel):
    """Schema base para SOFIPO."""
    nombre: str = Field(..., description="Nombre de la SOFIPO")
    gat_nominal: Optional[Decimal] = Field(None, description="GAT nominal")
    gat_real: Optional[Decimal] = Field(None, description="GAT real")
    fecha_actualizacion: date = Field(..., description="Fecha de actualización")


class SofipoCreate(SofipoBase):
    """Schema para crear una SOFIPO."""
    pass


class SofipoResponse(SofipoBase):
    """Schema para respuesta básica de API (sin plazos nested)."""
    id: int

    model_config = ConfigDict(from_attributes=True)


class SofipoWithPlazos(SofipoResponse):
    """Schema para respuesta con plazos nested."""
    plazos: list[SofipoPlazoResponse] = []

    model_config = ConfigDict(from_attributes=True)


class SofipoComparison(BaseModel):
    """Schema para comparación de SOFIPOs."""
    ranking: int
    sofipo: SofipoWithPlazos
    mejor_plazo: Optional[dict] = None  # {"plazo": 28, "tasa": 8.5}
```

### 3. Actualizar `app/models/__init__.py`

```python
# Archivo: app/models/__init__.py
"""
Importar todos los modelos para que Alembic los detecte.
"""

from app.models.cetes import Cetes
from app.models.sofipos import Sofipo, SofipoPlazo

__all__ = ["Cetes", "Sofipo", "SofipoPlazo"]
```

### 4. Crear migración
```bash
alembic revision --autogenerate -m "add sofipos tables"
```

### 5. Revisar migración
```bash
# Ver archivo generado
cat alembic/versions/*_add_sofipos_tables.py
```

### 6. Aplicar migración
```bash
alembic upgrade head
```

### 7. Verificar en PostgreSQL
```bash
psql -U postgres -d financial_rates -c "\d sofipos"
psql -U postgres -d financial_rates -c "\d sofipo_plazos"
```

## Criterios de Aceptación

- [ ] Modelos `Sofipo` y `SofipoPlazo` funcionan
  ```python
  from app.models.sofipos import Sofipo, SofipoPlazo
  print(Sofipo.__tablename__)  # "sofipos"
  print(SofipoPlazo.__tablename__)  # "sofipo_plazos"
  ```

- [ ] Relationship funciona correctamente
  ```python
  # Acceso a plazos desde Sofipo:
  sofipo.plazos  # lista de SofipoPlazo
  # Acceso a Sofipo desde Plazo:
  plazo.sofipo  # objeto Sofipo
  ```

- [ ] Schemas Pydantic con nested data
  ```python
  from app.schemas.sofipos import SofipoWithPlazos
  # Debe tener campo 'plazos' tipo list
  ```

- [ ] Migración aplicada
  ```bash
  alembic history --verbose
  ```

## Script de prueba

```python
# Archivo: test_sofipos_model.py (temporal)
from datetime import date
from app.database import SessionLocal
from app.models.sofipos import Sofipo, SofipoPlazo

db = SessionLocal()

# Crear SOFIPO
sofipo = Sofipo(
    nombre="Caja Popular Mexicana",
    gat_nominal=8.5,
    gat_real=4.5,
    fecha_actualizacion=date.today()
)
db.add(sofipo)
db.commit()
db.refresh(sofipo)

print(f"✓ SOFIPO creada: {sofipo}")

# Agregar plazos
plazos_data = [
    {"plazo": 28, "tasa": 8.0},
    {"plazo": 91, "tasa": 8.3},
    {"plazo": 182, "tasa": 8.5}
]

for p in plazos_data:
    plazo = SofipoPlazo(
        sofipo_id=sofipo.id,
        plazo=p["plazo"],
        tasa=p["tasa"],
        fecha_actualizacion=date.today()
    )
    db.add(plazo)

db.commit()

# Consultar con relationship
sofipo_con_plazos = db.query(Sofipo).filter(Sofipo.id == sofipo.id).first()
print(f"✓ SOFIPO con {len(sofipo_con_plazos.plazos)} plazos")
for p in sofipo_con_plazos.plazos:
    print(f"  - Plazo {p.plazo} días: {p.tasa}%")

db.close()
```

## Test de Pydantic nested

```python
# Test de schema nested
from app.schemas.sofipos import SofipoWithPlazos, SofipoPlazoResponse

# Simular ORM object
class MockSofipo:
    id = 1
    nombre = "Test SOFIPO"
    gat_nominal = 8.5
    gat_real = 4.5
    fecha_actualizacion = date.today()
    plazos = [
        type('obj', (object,), {
            'id': 1, 'sofipo_id': 1, 'plazo': 28,
            'tasa': 8.0, 'fecha_actualizacion': date.today()
        })
    ]

# Convertir a Pydantic
sofipo_schema = SofipoWithPlazos.model_validate(MockSofipo())
print(sofipo_schema.model_dump_json(indent=2))
```

## Notas adicionales

- `cascade="all, delete-orphan"` asegura que al eliminar SOFIPO se eliminen sus plazos
- `ondelete="CASCADE"` en la foreign key es redundante con cascade de SQLAlchemy, pero es buena práctica
- Los schemas nested son útiles para endpoints que devuelven datos relacionados

## Troubleshooting

**Error: "could not determine join condition"**
- Verificar que `back_populates` en ambos modelos apunta correctamente

**Migración no detecta foreign key**
- Importar los modelos en `alembic/env.py`

## Próximas tareas
➡️ [05] Modelos SQLAlchemy - CETES (si aún no se hizo)
➡️ [07] Modelos SQLAlchemy - Fondos/ETFs (paralelo)
