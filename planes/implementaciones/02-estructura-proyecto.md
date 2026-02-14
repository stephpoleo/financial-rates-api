# [02] Estructura del Proyecto

**Estado**: ⬜ Pendiente
**Dependencias**: [01] Setup Inicial
**Tipo**: 🔴 Secuencial
**Duración estimada**: 20 minutos

## Descripción
Crear la estructura de directorios y archivos `__init__.py` necesarios para el proyecto Python.

## Prerequisitos
- Tarea [01] completada
- Entorno virtual activado

## Estructura a crear

```
financial-rates-api/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   └── __init__.py
│   ├── schemas/
│   │   └── __init__.py
│   ├── collectors/
│   │   └── __init__.py
│   └── routers/
│       └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   └── __init__.py
│   └── integration/
│       └── __init__.py
├── alembic/
├── planes/
│   ├── plan-completo.md
│   └── implementaciones/
│       └── (estos archivos)
└── database/
```

## Pasos de implementación

### 1. Crear estructura de directorios
```bash
# Desde la raíz del proyecto (financial-rates-api/)
mkdir -p app/models app/schemas app/collectors app/routers
mkdir -p tests/unit tests/integration
mkdir -p alembic database
```

### 2. Crear archivos __init__.py
**Windows:**
```bash
type nul > app\__init__.py
type nul > app\models\__init__.py
type nul > app\schemas\__init__.py
type nul > app\collectors\__init__.py
type nul > app\routers\__init__.py
type nul > tests\__init__.py
type nul > tests\unit\__init__.py
type nul > tests\integration\__init__.py
```

**Linux/Mac:**
```bash
touch app/__init__.py
touch app/models/__init__.py
touch app/schemas/__init__.py
touch app/collectors/__init__.py
touch app/routers/__init__.py
touch tests/__init__.py
touch tests/unit/__init__.py
touch tests/integration/__init__.py
```

### 3. Crear README.md básico
```markdown
# Financial Rates API

Sistema Python que recopila diariamente rendimientos de CETES, SOFIPOs, fondos de inversión y ETFs (mexicanos e internacionales), los almacena en base de datos y expone una API REST para consultas.

## Características

- 📊 Recopilación automática de tasas de CETES desde API oficial de Banxico
- 🕷️ Web scraping de rendimientos de SOFIPOs
- 🌍 Integración con APIs de fondos y ETFs internacionales
- 🚀 API REST con FastAPI
- 🗄️ Almacenamiento en PostgreSQL
- ⏰ Actualizaciones diarias automatizadas

## Stack Tecnológico

- **Backend**: Python 3.11+, FastAPI
- **Base de datos**: PostgreSQL 14+
- **ORM**: SQLAlchemy 2.0
- **Scraping**: BeautifulSoup4
- **Scheduler**: APScheduler
- **Testing**: Pytest

## Estado del proyecto

🚧 En desarrollo - Ver `planes/implementaciones/` para progreso detallado

## Documentación

- [Plan completo](planes/plan-completo.md)
- [Guía de implementación](planes/implementaciones/LEEME.md)
```

### 4. Verificar estructura
```bash
tree -L 3  # Linux/Mac
# O en Windows:
tree /F
```

## Criterios de Aceptación

- [ ] Estructura de directorios completa
  ```bash
  ls -R  # Ver toda la estructura
  ```
- [ ] Todos los `__init__.py` creados en directorios Python
  ```bash
  find . -name "__init__.py"  # Debe listar 8 archivos
  ```
- [ ] README.md existe y tiene contenido básico
  ```bash
  cat README.md
  ```
- [ ] Directorio `database/` creado para scripts SQL
- [ ] Directorio `alembic/` creado (vacío por ahora)

## Notas adicionales

- Los archivos `__init__.py` permiten que Python trate los directorios como paquetes
- La estructura es escalable y sigue convenciones de proyectos FastAPI
- Los directorios `planes/` y `planes/implementaciones/` ya existen de tareas anteriores

## Próxima tarea
➡️ [03] Base de Datos - Schema
