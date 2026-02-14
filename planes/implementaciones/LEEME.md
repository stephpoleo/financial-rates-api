# Guía de Implementaciones - Financial Rates API

Bienvenido a la guía de implementación del proyecto Financial Rates API. Este directorio contiene 17 implementaciones individuales que desglosan el proyecto en tareas manejables y organizadas.

## 📋 Índice de Implementaciones

| ID | Nombre | Tipo | Dependencias | Duración |
|----|--------|------|--------------|----------|
| [01](01-setup-inicial.md) | Setup Inicial | 🔴 Secuencial | - | 30 min |
| [02](02-estructura-proyecto.md) | Estructura del Proyecto | 🔴 Secuencial | 01 | 20 min |
| [03](03-base-datos.md) | Base de Datos - Schema | 🔴 Secuencial | 02 | 30 min |
| [04](04-config-env.md) | Configuración y Environment | 🔴 Secuencial | 03 | 30 min |
| [05](05-models-cetes.md) | Modelos SQLAlchemy - CETES | 🟢 Paralelo | 04 | 45 min |
| [06](06-models-sofipos.md) | Modelos SQLAlchemy - SOFIPOs | 🟢 Paralelo | 04 | 45 min |
| [07](07-models-fondos.md) | Modelos SQLAlchemy - Fondos/ETFs | 🟢 Paralelo | 04 | 40 min |
| [08](08-collector-banxico.md) | Collector Banxico - CETES | 🟢 Paralelo | 05 | 2 horas |
| [09](09-collector-sofipos.md) | Scraper SOFIPOs | 🟢 Paralelo | 06 | 3 horas |
| [10](10-collector-etfs.md) | Collector ETFs | 🟢 Paralelo | 07 | 2 horas |
| [11](11-scheduler.md) | Scheduler | 🔴 Secuencial | 08,09,10 | 1.5 horas |
| [12](12-api-cetes.md) | Router API - CETES | 🟢 Paralelo | 11 | 1.5 horas |
| [13](13-api-sofipos.md) | Router API - SOFIPOs | 🟢 Paralelo | 11 | 1.5 horas |
| [14](14-api-fondos.md) | Router API - Fondos/ETFs | 🟢 Paralelo | 11 | 1.5 horas |
| [15](15-api-comparar.md) | Router API - Comparación | 🔴 Secuencial | 12,13,14 | 2 horas |
| [16](16-tests.md) | Tests & Documentación | 🟢 Paralelo | 12-15 | 3 horas |
| [17](17-docker-deploy.md) | Docker & Deployment | 🟢 Paralelo | 12-15 | 2 horas |

**Total estimado**: ~23 horas (menos si se trabaja en paralelo)

## 📊 Grafo de Dependencias

```
NIVEL 1 (Fundación - Secuencial)
├─ [01] Setup Inicial
└─ [02] Estructura Proyecto
   └─ [03] Base de Datos
      └─ [04] Config & Environment
         │
NIVEL 2 (Modelos - Paralelo) ───────┐
├─ [05] Model CETES                 │
├─ [06] Model SOFIPOs              │ Estos 3 pueden
└─ [07] Model Fondos/ETFs          │ hacerse en paralelo
   │                                │
NIVEL 3 (Collectors - Paralelo) ────┤
├─ [08] Collector Banxico          │
├─ [09] Scraper SOFIPOs            │ Estos 3 pueden
└─ [10] Collector ETFs             │ hacerse en paralelo
   │                                │
NIVEL 4 (Scheduler - Secuencial)    │
└─ [11] Scheduler                   │
   │                                │
NIVEL 5 (API Routers - Paralelo) ───┤
├─ [12] Router CETES               │
├─ [13] Router SOFIPOs             │ Estos 3 pueden
└─ [14] Router Fondos              │ hacerse en paralelo
   │                                │
NIVEL 6 (Comparación - Secuencial)  │
└─ [15] Router Comparar            │
   │                                │
NIVEL 7 (Finalización - Paralelo) ──┘
├─ [16] Tests & Docs
└─ [17] Docker & Deploy
```

## 🚀 Cómo Usar Esta Guía

### 1. Flujo Secuencial (1 persona)
Si trabajas solo, sigue este orden:
1. Completar tareas 01-04 (Fundación)
2. Completar tareas 05-07 (Modelos)
3. Completar tareas 08-10 (Collectors)
4. Completar tarea 11 (Scheduler)
5. Completar tareas 12-14 (API)
6. Completar tarea 15 (Comparación)
7. Completar tareas 16-17 (Tests y Docker)

### 2. Flujo Paralelo (Equipo)
Si trabajan en equipo:

**Sprint 1 - Fundación** (Secuencial)
- 1 persona hace 01-04 en orden

**Sprint 2 - Modelos** (Paralelo)
- Persona A: [05] CETES
- Persona B: [06] SOFIPOs
- Persona C: [07] Fondos

**Sprint 3 - Recopiladores** (Paralelo)
- Persona A: [08] Collector Banxico
- Persona B: [09] Scraper SOFIPOs
- Persona C: [10] Collector ETFs

**Sprint 4 - Scheduler** (Secuencial)
- 1 persona hace [11]

**Sprint 5 - API** (Paralelo + Secuencial)
- Personas A,B,C hacen [12], [13], [14] en paralelo
- Luego 1 persona hace [15]

**Sprint 6 - Finalización** (Paralelo)
- Persona A: [16] Tests
- Persona B: [17] Docker

### 3. Formato de Cada Archivo

Cada archivo de implementación incluye:
- ✅ **Estado**: Para marcar progreso
- 📦 **Dependencias**: Qué tareas deben completarse antes
- 🏷️ **Tipo**: Secuencial (🔴) o Paralelo (🟢)
- ⏱️ **Duración estimada**
- 📝 **Descripción** clara de la tarea
- 📁 **Archivos** a crear/modificar
- 🔧 **Pasos de implementación** detallados
- ✅ **Criterios de aceptación** verificables
- 🧪 **Comandos de verificación**

## 📌 Marcar Progreso

Puedes marcar cada implementación editando el archivo:

```markdown
**Estado**: ✅ Completada
```

O llevar control en esta tabla:

| Sprint | Tareas | Estado |
|--------|--------|--------|
| 1 | 01-04 | ⬜ |
| 2 | 05-07 | ⬜ |
| 3 | 08-10 | ⬜ |
| 4 | 11 | ⬜ |
| 5 | 12-15 | ⬜ |
| 6 | 16-17 | ⬜ |

## 🔑 API Keys Necesarias

Durante la implementación necesitarás obtener:

| Servicio | Tarea | URL | Costo |
|----------|-------|-----|-------|
| Banxico SIE | [08] | https://www.banxico.org.mx/SieAPIRest/service/v1/?locale=en | Gratuito |
| Alpha Vantage | [10] | https://www.alphavantage.co/support/#api-key | Gratuito (25 req/día) |

## 🎯 Hitos del Proyecto

- ✅ **Hito 1**: Después de [04] - Proyecto configurado
- ✅ **Hito 2**: Después de [07] - Modelos de datos completos
- ✅ **Hito 3**: Después de [10] - Datos fluyendo a la DB
- ✅ **Hito 4**: Después de [11] - Sistema automatizado
- ✅ **Hito 5**: Después de [15] - API REST completa
- ✅ **Hito 6**: Después de [17] - Proyecto deployable

## 📚 Recursos Adicionales

- **Plan Completo**: Ver `../plan-completo.md` para contexto general
- **Documentación Técnica**: Cada implementación referencia secciones específicas del plan completo
- **Troubleshooting**: Cada archivo incluye sección de solución de problemas

## 💡 Consejos

1. **Lee el plan completo primero**: `planes/plan-completo.md` para entender el contexto general
2. **No te saltes dependencias**: Respeta el orden de dependencias
3. **Verifica criterios de aceptación**: Cada tarea tiene criterios claros
4. **Usa los comandos de verificación**: Están probados y funcionan
5. **Haz commits frecuentes**: Después de cada tarea completada
6. **Documenta cambios**: Si modificas algo del plan original

## 🐛 Reporte de Problemas

Si encuentras errores o mejoras en las implementaciones:
1. Documenta el problema en el archivo correspondiente
2. Sugiere la solución
3. Actualiza el archivo con la corrección

## 🎉 ¿Listo para Empezar?

1. Asegúrate de tener Python 3.11+ y PostgreSQL instalados
2. Abre [01-setup-inicial.md](01-setup-inicial.md)
3. Sigue los pasos
4. ¡Marca como completado y continúa con la siguiente!

---

**Última actualización**: 2026-02-03
**Versión**: 1.0
