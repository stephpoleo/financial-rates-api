# [16] Tests & Documentación

**Estado**: ⬜ Pendiente | **Dependencias**: [12-15] | **Tipo**: 🟢 Paralelo | **Duración**: 3 horas

## Descripción
Completar suite de tests y documentación del proyecto.

## Archivos
- `tests/` (completar)
- `README.md` (actualizar)
- `docs/API.md` (crear)
- `docs/SETUP.md` (crear)

## Tests
```bash
# Cobertura >80%
pytest --cov=app --cov-report=html tests/

# Tests unitarios
pytest tests/unit/ -v

# Tests integración
pytest tests/integration/ -v
```

## Documentación
- **README.md**: Descripción, features, instalación, uso
- **docs/API.md**: Todos los endpoints con ejemplos
- **docs/SETUP.md**: Setup paso a paso, troubleshooting

## Criterios de Aceptación
- [ ] Cobertura >80%
- [ ] Todos tests pasan
- [ ] README completo
- [ ] Documentación API detallada

➡️ **Próxima**: [17] Docker & Deployment (paralelo)
