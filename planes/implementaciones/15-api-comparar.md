# [15] Router API - Comparación

**Estado**: ⬜ Pendiente | **Dependencias**: [12], [13], [14] | **Tipo**: 🔴 Secuencial | **Duración**: 2 horas

## Descripción
Implementar endpoint para comparar rendimientos entre CETES, SOFIPOs y Fondos.

## Archivos
- `app/routers/comparar.py`
- `app/schemas/comparar.py`
- `app/main.py` (actualizar)
- `tests/integration/test_comparar_api.py`

## Endpoints
- `GET /api/comparar` - Comparación general
- `GET /api/comparar/plazo/{dias}` - Comparar por plazo similar

## Schema ComparacionResponse
```python
{
  "cetes": [...],
  "sofipos_top": [...],  # Top 5
  "fondos_top": [...],   # Top 5
  "mejor_opcion": {
    "tipo": "SOFIPO",
    "nombre": "...",
    "rendimiento": 8.5,
    "liquidez": "alta",
    "riesgo": "medio"
  }
}
```

## Lógica de "Mejor Opción"
Considerar:
- Rendimiento (principal)
- Liquidez (CETES > SOFIPOs > Fondos)
- Riesgo (CETES < SOFIPOs < Fondos)

## Criterios de Aceptación
- [ ] Retorna comparación completa
- [ ] Lógica de "mejor opción" funciona
- [ ] Response bien estructurado
- [ ] Tests pasan

## Verificación
```bash
curl http://localhost:8000/api/comparar
curl http://localhost:8000/api/comparar/plazo/28
```

➡️ **Próxima**: [16] Tests & Documentación (paralelo)
