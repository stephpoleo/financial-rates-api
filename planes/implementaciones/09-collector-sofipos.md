# [09] Scraper SOFIPOs

**Estado**: ⬜ Pendiente | **Dependencias**: [06] | **Tipo**: 🟢 Paralelo | **Duración**: 3 horas

## Descripción
Implementar web scraper para obtener rendimientos de SOFIPOs desde Tasas.mx

## Archivos
- `app/collectors/sofipo_scraper.py`
- `tests/unit/test_sofipo_scraper.py`

## Dependencias
```txt
beautifulsoup4==4.12.3
lxml==5.1.0
```

## Fuente de Datos
- URL: https://www.tasas.mx/
- Verificar `robots.txt` antes de scrapear
- Implementar rate limiting (1-2 segundos entre requests)

## Implementación Clave
Clase `SofipoScraper` con:
- `fetch_html(url)`: GET con User-Agent apropiado
- `parse_sofipos(html)`: Extraer datos de tabla HTML
- `parse_plazos(html, sofipo_id)`: Extraer rendimientos por plazo
- `save_to_db(session, data)`: Guardar en tablas `sofipos` y `sofipo_plazos`

## Criterios de Aceptación
- [ ] Scrapea datos de Tasas.mx exitosamente
- [ ] Extrae SOFIPOs con GAT nominal y real
- [ ] Extrae rendimientos por plazo
- [ ] Respeta rate limiting
- [ ] Tests con HTML mock pasan

## Verificación
```bash
python -m app.collectors.sofipo_scraper
psql -U postgres -d financial_rates -c "SELECT * FROM sofipos LIMIT 5;"
```

➡️ **Próxima**: [10] Collector ETFs (paralelo)
