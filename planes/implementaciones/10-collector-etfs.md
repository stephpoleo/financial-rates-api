# [10] Collector ETFs

**Estado**: ⬜ Pendiente | **Dependencias**: [07] | **Tipo**: 🟢 Paralelo | **Duración**: 2 horas

## Descripción
Implementar collector para fondos/ETFs desde API externa (Alpha Vantage).

## Obtener API Key
1. Registrarse: https://www.alphavantage.co/support/#api-key
2. Tier gratuito: 25 requests/día
3. Agregar a `.env`: `ALPHA_VANTAGE_API_KEY=tu_key`

## Archivos
- `app/collectors/etf_collector.py`
- `app/collectors/tickers.json`
- `tests/unit/test_etf_collector.py`

## Tickers Iniciales (tickers.json)
```json
{
  "etfs": [
    {"ticker": "SPY", "name": "SPDR S&P 500", "market": "US"},
    {"ticker": "QQQ", "name": "Invesco QQQ", "market": "US"},
    {"ticker": "VOO", "name": "Vanguard S&P 500", "market": "US"}
  ]
}
```

## Implementación Clave
Clase `ETFCollector` con:
- `get_etf_data(ticker)`: Obtener datos de ticker específico
- `calculate_performance(data)`: Calcular rendimientos
- `save_to_db(data)`: Guardar en tabla `fondos_etfs`
- Rate limiting: 5 requests/min (tier gratuito)

## Criterios de Aceptación
- [ ] Obtiene datos de Alpha Vantage
- [ ] Calcula rendimientos correctamente
- [ ] Respeta rate limits (sleep entre requests)
- [ ] Tests con mocks pasan

## Verificación
```bash
python -m app.collectors.etf_collector
psql -U postgres -d financial_rates -c "SELECT ticker, rendimiento_anual FROM fondos_etfs;"
```

➡️ **Próxima**: [11] Scheduler (secuencial, requiere 08,09,10)
