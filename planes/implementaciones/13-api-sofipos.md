# [13] Router API - SOFIPOs

**Estado**: ⬜ Pendiente | **Dependencias**: [11] | **Tipo**: 🟢 Paralelo | **Duración**: 1.5 horas

## Descripción
Implementar endpoints REST para consultar datos de SOFIPOs con paginación.

## Archivos
- `app/routers/sofipos.py`
- `app/main.py` (actualizar)
- `tests/integration/test_sofipos_api.py`

## Endpoints
- `GET /api/sofipos?limit=10&offset=0` - Listar SOFIPOs con paginación
- `GET /api/sofipos/{sofipo_id}` - Detalle con plazos nested
- `GET /api/sofipos/top?n=10` - Top SOFIPOs por GAT

## Criterios de Aceptación
- [ ] Paginación funciona correctamente
- [ ] Nested data (plazos) se retorna en detalle
- [ ] Ordenamiento por GAT funciona
- [ ] Tests pasan

## Verificación
```bash
curl "http://localhost:8000/api/sofipos?limit=5"
curl http://localhost:8000/api/sofipos/1
curl "http://localhost:8000/api/sofipos/top?n=5"
```

➡️ **Próxima**: [14] Router API - Fondos (paralelo)
