# [11] Scheduler

**Estado**: ⬜ Pendiente | **Dependencias**: [08], [09], [10] | **Tipo**: 🔴 Secuencial | **Duración**: 1.5 horas

## Descripción
Implementar scheduler para ejecutar collectors automáticamente en horarios específicos.

## Archivos
- `app/scheduler.py`
- `app/main.py` (actualizar)

## Dependencias
```txt
apscheduler==3.10.4
```

## Horarios de Ejecución
- **CETES**: 11:00 AM (después de subasta, martes y jueves típicamente)
- **SOFIPOs**: 7:00 AM (inicio del día)
- **ETFs**: 8:00 PM (después cierre mercados)
- **Timezone**: America/Mexico_City

## Implementación Clave
```python
from apscheduler.schedulers.background import BackgroundScheduler
from app.collectors.banxico_collector import BanxicoCollector
from app.collectors.sofipo_scraper import SofipoScraper
from app.collectors.etf_collector import ETFCollector

scheduler = BackgroundScheduler(timezone="America/Mexico_City")

scheduler.add_job(BanxicoCollector().collect, 'cron', hour=11, minute=0)
scheduler.add_job(SofipoScraper().collect, 'cron', hour=7, minute=0)
scheduler.add_job(ETFCollector().collect, 'cron', hour=20, minute=0)

scheduler.start()
```

## Criterios de Aceptación
- [ ] Scheduler inicia correctamente
- [ ] Jobs se ejecutan en horarios configurados
- [ ] Logs muestran ejecuciones exitosas/fallidas
- [ ] Opción para ejecución manual inmediata

## Verificación
```bash
# Iniciar scheduler
python app/main.py

# Ver logs
tail -f logs/scheduler.log
```

➡️ **Próxima**: [12] Router API - CETES (paralelo)
