# [14] Router API - Fondos/ETFs

**Estado**: ⬜ Pendiente | **Dependencias**: [11] | **Tipo**: 🟢 Paralelo | **Duración**: 1.5 horas

## Descripción
Implementar endpoints REST para fondos/ETFs con filtros y búsqueda.

## Archivos
- `app/routers/fondos.py`
- `app/main.py` (actualizar)
- `tests/integration/test_fondos_api.py`

## Endpoints
- `GET /api/fondos?tipo=ETF&mercado=US&limit=10` - Listar con filtros
- `GET /api/fondos/{ticker}` - Detalle de fondo específico
- `GET /api/fondos/buscar?q=SPY` - Búsqueda por ticker o nombre

## Criterios de Aceptación
- [ ] Filtros por tipo y mercado funcionan
- [ ] Búsqueda con SQL LIKE/ILIKE funciona
- [ ] Ordenamiento por rendimiento funciona
- [ ] Tests pasan

## Verificación
```bash
curl "http://localhost:8000/api/fondos?mercado=US"
curl http://localhost:8000/api/fondos/SPY
curl "http://localhost:8000/api/fondos/buscar?q=vanguard"
```

➡️ **Próxima**: [15] Router API - Comparación (secuencial)
