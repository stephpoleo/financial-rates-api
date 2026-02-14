# [04] Configuración y Environment

**Estado**: ⬜ Pendiente
**Dependencias**: [03] Base de Datos - Schema
**Tipo**: 🔴 Secuencial
**Duración estimada**: 30 minutos

## Descripción
Implementar sistema de configuración centralizado usando Pydantic Settings para manejar variables de entorno de forma type-safe.

## Prerequisitos
- Tarea [03] completada
- Entorno virtual activado

## Archivos a crear/modificar
- `app/config.py` (crear)
- `.env` (crear, NO commitear)
- `.env.example` (actualizar)
- `requirements.txt` (actualizar)

## Pasos de implementación

### 1. Actualizar `requirements.txt`
```txt
# Agregar estas dependencias:
python-dotenv==1.0.0
pydantic==2.5.3
pydantic-settings==2.1.0
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Crear `app/config.py`

```python
# Archivo: app/config.py
"""
Configuración centralizada de la aplicación.
Usa Pydantic Settings para validación type-safe de variables de entorno.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Configuración de la aplicación."""

    # Base de datos
    DATABASE_URL: str

    # API Keys externas
    BANXICO_API_KEY: Optional[str] = None
    ALPHA_VANTAGE_API_KEY: Optional[str] = None

    # Configuración de la aplicación
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8000"]

    # Scheduler
    ENABLE_SCHEDULER: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


# Instancia global de settings
settings = Settings()


# Helper para generar DATABASE_URL para SQLAlchemy
def get_database_url() -> str:
    """
    Retorna la URL de la base de datos.
    SQLAlchemy 2.0 requiere 'postgresql://' no 'postgres://'
    """
    url = settings.DATABASE_URL
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return url
```

### 4. Crear archivo `.env`
```bash
# Archivo: .env
# IMPORTANTE: Este archivo NO debe estar en git

# Base de datos
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/financial_rates

# API Keys (obtener en tareas posteriores)
BANXICO_API_KEY=
ALPHA_VANTAGE_API_KEY=

# Configuración
ENVIRONMENT=development
LOG_LEVEL=DEBUG
API_HOST=0.0.0.0
API_PORT=8000

# Scheduler
ENABLE_SCHEDULER=true

# CORS
CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]
```

### 5. Actualizar `.env.example`
```bash
# Archivo: .env.example
# Template para configuración. Copiar a .env y llenar los valores.

# Base de datos
DATABASE_URL=postgresql://usuario:password@localhost:5432/financial_rates

# API Keys - Obtener de:
# Banxico: https://www.banxico.org.mx/SieAPIRest/service/v1/?locale=en
# Alpha Vantage: https://www.alphavantage.co/support/#api-key
BANXICO_API_KEY=tu_token_banxico_aqui
ALPHA_VANTAGE_API_KEY=tu_api_key_alpha_vantage_aqui

# Configuración de la aplicación
ENVIRONMENT=development
LOG_LEVEL=INFO
API_HOST=0.0.0.0
API_PORT=8000

# Scheduler (true/false)
ENABLE_SCHEDULER=true

# CORS - Lista de orígenes permitidos
CORS_ORIGINS=["http://localhost:3000"]
```

### 6. Verificar que `.env` está en `.gitignore`
```bash
grep -q "^\.env$" .gitignore && echo "OK" || echo ".env" >> .gitignore
```

### 7. Crear script de prueba
```python
# Archivo: test_config.py (temporal)
from app.config import settings, get_database_url

print("=== Configuración cargada ===")
print(f"Environment: {settings.ENVIRONMENT}")
print(f"Log Level: {settings.LOG_LEVEL}")
print(f"Database URL: {get_database_url()}")
print(f"API Port: {settings.API_PORT}")
print(f"Banxico API Key: {'✓ Configurada' if settings.BANXICO_API_KEY else '✗ No configurada'}")
print(f"Alpha Vantage Key: {'✓ Configurada' if settings.ALPHA_VANTAGE_API_KEY else '✗ No configurada'}")
print(f"Scheduler: {'Habilitado' if settings.ENABLE_SCHEDULER else 'Deshabilitado'}")
```

### 8. Ejecutar prueba
```bash
python test_config.py
```

## Criterios de Aceptación

- [ ] `app/config.py` funciona y carga variables
  ```bash
  python test_config.py
  ```

- [ ] Validación de Pydantic funcionando
  ```python
  # Si DATABASE_URL no está definida, debe fallar:
  # ValidationError: 1 validation error for Settings
  ```

- [ ] `.env` no está en git
  ```bash
  git status | grep .env
  # No debe aparecer .env (solo .env.example)
  ```

- [ ] `.env.example` documentado con todos los campos

- [ ] Dependencias instaladas correctamente
  ```bash
  pip list | grep pydantic
  ```

## Uso en el código

```python
# En cualquier parte del proyecto:
from app.config import settings

# Acceder a configuración
db_url = settings.DATABASE_URL
api_key = settings.BANXICO_API_KEY

# Type-safe, con autocompletado en IDE
```

## Notas adicionales

- Pydantic Settings valida tipos automáticamente
- Variables de entorno sobrescriben valores en `.env`
- El patrón singleton `settings = Settings()` asegura una sola instancia
- `Optional[str]` permite que API keys no estén definidas inicialmente

## Troubleshooting

**Error: "field required"**
- Verificar que `.env` existe y tiene la variable
- Verificar nombre de variable (case-sensitive)

**API keys vacías**
- Es normal al inicio, se configurarán en tareas [08] y [10]

## Próxima tarea
➡️ [05] Modelos SQLAlchemy - CETES (puede hacerse en paralelo con [06] y [07])
