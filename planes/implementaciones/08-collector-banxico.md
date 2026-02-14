# [08] Collector Banxico - CETES

**Estado**: ⬜ Pendiente | **Dependencias**: [05] | **Tipo**: 🟢 Paralelo | **Duración**: 2 horas

## Descripción
Implementar recopilador de datos de CETES desde API oficial de Banxico SIE.

## Obtener API Token
1. Visitar: https://www.banxico.org.mx/SieAPIRest/service/v1/?locale=en
2. Solicitar token (gratuito, llega por email)
3. Agregar a `.env`: `BANXICO_API_KEY=tu_token`

## IDs de Series CETES
- 28 días: SF43936
- 91 días: SF43939
- 182 días: SF43942
- 364 días: SF43945

## Archivos
- `app/collectors/banxico_collector.py`
- `tests/unit/test_banxico_collector.py`

## Dependencias
```txt
requests==2.31.0
loguru==0.7.2
```

## Implementación Clave
Ver plan-completo.md sección "[08]" para código completo del collector que incluye:
- Clase `BanxicoCollector` con métodos `get_cetes_rate()`, `get_all_cetes()`, `save_to_db()`
- Manejo de errores HTTP y logging
- Tests unitarios con mocks

## Criterios de Aceptación
- [ ] Obtiene datos de API de Banxico correctamente
- [ ] Guarda en tabla `cetes` sin duplicados
- [ ] Logs informativos
- [ ] Tests unitarios pasan: `pytest tests/unit/test_banxico_collector.py`

## Verificación
```bash
python -m app.collectors.banxico_collector
psql -U postgres -d financial_rates -c "SELECT * FROM cetes LIMIT 5;"
```

➡️ **Próxima**: [09] Scraper SOFIPOs (paralelo)
