# [01] Setup Inicial

**Estado**: ⬜ Pendiente
**Dependencias**: Ninguna
**Tipo**: 🔴 Secuencial
**Duración estimada**: 30 minutos

## Descripción
Configurar el entorno de desarrollo básico con Python y PostgreSQL.

## Archivos a crear
- `requirements.txt`
- `.env.example`
- `.gitignore`

## Pasos de implementación

### 1. Verificar/Instalar Python 3.11+
```bash
python --version  # Debe ser 3.11 o superior
```
Si no está instalado, descargar de https://www.python.org/downloads/

### 2. Instalar PostgreSQL 14+
**Opción A - Local:**
- Descargar de https://www.postgresql.org/download/
- Instalar y configurar

**Opción B - Docker:**
```bash
docker run --name postgres-financial -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:14
```

### 3. Crear directorio del proyecto
```bash
cd C:\Users\steph\Github
mkdir financial-rates-api
cd financial-rates-api
```

### 4. Crear entorno virtual
```bash
python -m venv venv
```

### 5. Activar entorno virtual
**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 6. Crear archivo `.gitignore`
```bash
# Archivo: .gitignore
venv/
__pycache__/
*.pyc
.env
.pytest_cache/
*.db
*.sqlite
htmlcov/
.coverage
*.log
.DS_Store
alembic/versions/*.pyc
```

### 7. Crear archivo `requirements.txt` inicial
```bash
# Archivo: requirements.txt
# Este archivo se irá llenando en las siguientes tareas
```

### 8. Crear archivo `.env.example`
```bash
# Archivo: .env.example
# Configuración de base de datos
DATABASE_URL=postgresql://usuario:password@localhost:5432/financial_rates

# API Keys (obtener en las tareas correspondientes)
BANXICO_API_KEY=tu_token_aqui
ALPHA_VANTAGE_API_KEY=tu_api_key_aqui

# Configuración de la aplicación
ENVIRONMENT=development
LOG_LEVEL=INFO
```

## Criterios de Aceptación

- [ ] Python 3.11+ instalado y funcionando
  ```bash
  python --version
  ```
- [ ] PostgreSQL corriendo
  ```bash
  psql --version
  # O si usas Docker:
  docker ps | grep postgres-financial
  ```
- [ ] Entorno virtual creado y activado
  ```bash
  which python  # Debe mostrar ruta dentro de venv/
  ```
- [ ] Archivos base creados (`.gitignore`, `requirements.txt`, `.env.example`)
  ```bash
  ls -la
  ```

## Notas adicionales

- El entorno virtual debe estar activado para todas las tareas siguientes
- PostgreSQL debe estar corriendo antes de continuar con tareas de base de datos
- Mantener `.env` fuera del control de versiones (incluido en `.gitignore`)

## Próxima tarea
➡️ [02] Estructura del Proyecto
