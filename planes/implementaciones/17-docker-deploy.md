# [17] Docker & Deployment

**Estado**: ⬜ Pendiente | **Dependencias**: [12-15] | **Tipo**: 🟢 Paralelo | **Duración**: 2 horas

## Descripción
Containerizar aplicación y preparar para deployment con Docker.

## Archivos
- `Dockerfile`
- `docker-compose.yml`
- `.dockerignore`
- `docs/DEPLOYMENT.md`

## Dockerfile
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## docker-compose.yml
```yaml
version: '3.8'
services:
  postgres:
    image: postgres:14
    environment:
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: financial_rates
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  api:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - postgres
    environment:
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/financial_rates
    env_file:
      - .env

volumes:
  postgres_data:
```

## Criterios de Aceptación
- [ ] Docker build exitoso: `docker-compose build`
- [ ] Aplicación corre: `docker-compose up -d`
- [ ] Accesible en container: `curl http://localhost:8000/api/cetes`
- [ ] Base de datos persiste con volumes
- [ ] Documentación deployment completa

## Verificación
```bash
docker-compose up -d
docker-compose logs -f api
curl http://localhost:8000/docs
```

✅ **Proyecto completo!**
