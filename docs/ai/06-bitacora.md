# 06 · Bitácora de sesiones

> Historial **solo de agregar**, la entrada más reciente arriba. Máximo 10 líneas por sesión.
> Los agentes **no necesitan leer este archivo** al iniciar; solo lo actualizan al cerrar. Sirve a la pareja para seguir el progreso, medir cuánto rinde el desarrollo asistido por IA, documentar el uso de IA si el docente lo pide y hacer la retro (F4-07).

## Formato

```markdown
### Sesión N · AAAA-MM-DD · Fx-NN

- **Persona / agente:** quién condujo y qué agente/modelo se usó
- **Hecho:** …
- **Pruebas:** comando → resultado
- **Commits:** hash corto + mensaje
- **Tiempo:** horas reales (comparar con la estimación de 2–3 h)
- **Correcciones humanas a la IA:** qué se tuvo que corregir (conocimiento, lógica, estilo)
- **Siguiente:** Fx-NN
```

---

### Sesión 1 · 2026-10-21 · F3-Cierre

- **Persona / agente:** Pareja / Antigravity AI
- **Hecho:** Implementación completa de `base_conocimiento.pl` (66 hechos aridad 2, 17 reglas en 3 niveles), `motor_inferencia.py` (puente PySwip) y `pruebas.py` (5 casos de prueba formateados). Sincronización de artefactos (ficha, matriz, diccionario de predicados y evidencias fotográficas).
- **Pruebas:** `python3 pruebas.py` → 5/5 PASS; `swipl consult` sin advertencias.
- **Commits:** Pendiente (listo para commit inicial del entregable).
- **Tiempo:** ~1.5 h
- **Correcciones humanas a la IA:** Ajuste de nombres de evidencias a formato estándar; corrección del catálogo de predicados desfasado en documentación.
- **Siguiente:** Preparar PDF de Ficha de Proyecto para entrega final.

---

### Sesión 0 · 2026-10-21 · F0-00

- **Persona / agente:** Claude
- **Hecho:** paquete de documentación y plan de desarrollo para DiagnostiPC a partir del Entregable 1 y de los requisitos técnicos del curso.
- **Pruebas:** no aplica (solo documentación).
- **Commits:** pendiente (primer commit del repositorio).
- **Tiempo:** n/a
- **Correcciones humanas a la IA:** n/a
- **Siguiente:** F0-01
