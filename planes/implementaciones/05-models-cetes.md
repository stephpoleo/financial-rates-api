# [05] Modelos SQLAlchemy - CETES

**Estado**: ⬜ Pendiente
**Dependencias**: [04] Configuración y Environment
**Tipo**: 🟢 Paralelo (con [06], [07])
**Duración estimada**: 45 minutos

## Descripción
Implementar modelo ORM de SQLAlchemy para la tabla CETES, configurar Alembic para migraciones, y crear schemas Pydantic para validación.

## Prerequisitos
- Tarea [04] completada
- PostgreSQL con tablas creadas

## Archivos a crear
- `app/database.py` (crear)
- `app/models/cetes.py` (crear)
- `app/schemas/cetes.py` (crear)
- `alembic.ini` (configurar)
- `alembic/env.py` (configurar)

## Pasos de implementación

### 1. Actualizar `requirements.txt`
```txt
# Agregar:
sqlalchemy==2.0.25
psycopg2-binary==2.9.9
alembic==1.13.1
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Crear `app/database.py`

```python
# Archivo: app/database.py
"""
Configuración de SQLAlchemy y sesión de base de datos.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import get_database_url

# Engine de SQLAlchemy
engine = create_engine(
    get_database_url(),
    pool_pre_ping=True,  # Verifica conexiones antes de usar
    echo=False  # Cambiar a True para debug SQL
)

# SessionLocal factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa para modelos
Base = declarative_base()


# Dependency para FastAPI
def get_db():
    """
    Dependency para inyectar sesión de DB en endpoints.

    Uso:
        @app.get("/endpoint")
        def endpoint(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 4. Crear `app/models/cetes.py`

```python
# Archivo: app/models/cetes.py
"""
Modelo ORM para tabla CETES.
"""

from sqlalchemy import Column, Integer, Numeric, Date, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Cetes(Base):
    """Modelo para tasas de CETES."""

    __tablename__ = "cetes"

    id = Column(Integer, primary_key=True, index=True)
    plazo = Column(Integer, nullable=False)  # 28, 91, 182, 364
    tasa = Column(Numeric(5, 2), nullable=False)
    fecha_subasta = Column(Date, nullable=False)
    fecha_vencimiento = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Cetes(plazo={self.plazo}, tasa={self.tasa}, fecha={self.fecha_subasta})>"
```

### 5. Crear `app/schemas/cetes.py`

```python
# Archivo: app/schemas/cetes.py
"""
Schemas Pydantic para validación de datos de CETES.
"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import date
from decimal import Decimal
from typing import Optional


class CetesBase(BaseModel):
    """Schema base de CETES."""
    plazo: int = Field(..., description="Plazo en días (28, 91, 182, 364)")
    tasa: Decimal = Field(..., description="Tasa de rendimiento")
    fecha_subasta: date = Field(..., description="Fecha de subasta")
    fecha_vencimiento: Optional[date] = Field(None, description="Fecha de vencimiento")


class CetesCreate(CetesBase):
    """Schema para crear un registro de CETES."""
    pass


class CetesResponse(CetesBase):
    """Schema para respuesta de API."""
    id: int

    model_config = ConfigDict(from_attributes=True)


class CetesHistorico(BaseModel):
    """Schema para consulta histórica."""
    plazo: int
    datos: list[CetesResponse]
```

### 6. Inicializar Alembic
```bash
alembic init alembic
```

### 7. Configurar `alembic.ini`

Buscar la línea `sqlalchemy.url` y comentarla:
```ini
# sqlalchemy.url = driver://user:pass@localhost/dbname
```

### 8. Configurar `alembic/env.py`

Modificar el archivo para usar nuestra configuración:

```python
# Archivo: alembic/env.py (modificar secciones)

# Agregar al inicio:
import sys
from pathlib import Path

# Agregar app/ al path
sys.path.append(str(Path(__file__).parent.parent))

from app.config import get_database_url
from app.database import Base

# Importar todos los modelos
from app.models.cetes import Cetes

# En la sección de configuración:
config = context.config
config.set_main_option("sqlalchemy.url", get_database_url())

# Asignar metadata:
target_metadata = Base.metadata
```

### 9. Crear primera migración
```bash
alembic revision --autogenerate -m "add cetes table"
```

### 10. Revisar migración generada
```bash
# Ver archivo generado en alembic/versions/
ls alembic/versions/
```

### 11. Aplicar migración
```bash
alembic upgrade head
```

### 12. Verificar en PostgreSQL
```bash
psql -U postgres -d financial_rates -c "\d cetes"
psql -U postgres -d financial_rates -c "SELECT * FROM alembic_version;"
```

## Criterios de Aceptación

- [ ] Modelo `Cetes` funciona con SQLAlchemy
  ```python
  from app.models.cetes import Cetes
  print(Cetes.__tablename__)  # debe imprimir "cetes"
  ```

- [ ] Schemas Pydantic validando correctamente
  ```python
  from app.schemas.cetes import CetesCreate
  from datetime import date

  cete = CetesCreate(
      plazo=28,
      tasa=6.90,
      fecha_subasta=date(2026, 2, 3)
  )
  print(cete.model_dump())
  ```

- [ ] Alembic configurado
  ```bash
  alembic current
  # Debe mostrar la versión actual
  ```

- [ ] Migración aplicada sin errores
  ```bash
  alembic history
  ```

- [ ] Tabla existe en PostgreSQL (puede tener estructura diferente si ya existía)

## Script de prueba

```python
# Archivo: test_cetes_model.py (temporal)
from datetime import date
from app.database import SessionLocal
from app.models.cetes import Cetes

# Crear sesión
db = SessionLocal()

# Crear un registro de prueba
cete = Cetes(
    plazo=28,
    tasa=6.90,
    fecha_subasta=date(2026, 2, 3)
)

db.add(cete)
db.commit()
db.refresh(cete)

print(f"✓ CETES creado: {cete}")

# Consultar
cetes = db.query(Cetes).filter(Cetes.plazo == 28).all()
print(f"✓ CETES encontrados: {len(cetes)}")

db.close()
```

## Notas adicionales

- SQLAlchemy 2.0 usa nueva sintaxis (no `query()` legacy)
- `ConfigDict(from_attributes=True)` permite convertir ORM → Pydantic
- Alembic trackea cambios en el schema automáticamente
- Las migraciones deben versionarse en git

## Troubleshooting

**Error: "Table already exists"**
- Si la tabla ya existe, Alembic no la recreará
- Usar `alembic downgrade -1` y `alembic upgrade head` para forzar

**Error de import**
- Verificar que `app/` está en el PYTHONPATH
- Verificar que todos los `__init__.py` existen

## Próximas tareas
➡️ [06] Modelos SQLAlchemy - SOFIPOs (paralelo)
➡️ [07] Modelos SQLAlchemy - Fondos/ETFs (paralelo)
