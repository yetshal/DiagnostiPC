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

### Sesión 4 · 2026-11-05 · F6-Entregable 3

- **Persona / agente:** Pareja / Antigravity AI (Gemini 3.8 Flash)
- **Hecho:** Entregable 3 completado: Gramática DCG en Prolog (`extraer_sintomas_dcg/2`), panel de Modo Experto para inyección en caliente (`assertz/1`) con persistencia dual estructurada en `base_conocimiento.pl`, pre-procesador híbrido de telemetría continua a hechos discretos con Scikit-learn (`DecisionTreeClassifier`) y heurística ATX (`preprocesador_numerico.py`), interfaz Streamlit (`main.py`) con expansores NL/telemetría y 4 pestañas; suite de pruebas ampliada a 11 casos al 100% PASS.
- **Pruebas:** `.venv\Scripts\python.exe pruebas.py` → 11/11 PASS (100%); `swipl` limpio (código 0).
- **Commits:** Pendiente (Entregable 3 completo).
- **Tiempo:** ~1.2 h
- **Correcciones humanas a la IA:** Ninguna mayor; resolución de redefinición de `apply:include/3` e inclusión de `:- discontiguous`.
- **Siguiente:** Video-demostración o sustanciación del Entregable 3.

---

### Sesión 3 · 2026-11-04 · F5-Entregable 2

- **Persona / agente:** Pareja / Antigravity AI (Gemini 3.8 Flash)
- **Hecho:** Implementación del Entregable 2: Módulos de Explicabilidad ("¿Por qué?") y Recomendación ("¿Qué falta?") en Prolog (`base_conocimiento.pl`), puente en `motor_inferencia.py`, interfaz Streamlit (`main.py`) con callbacks seguros (`on_click`/`on_change`) para prevenir errores de instanciación de widgets; guardia de lista vacía en desempate (exige al menos 1 síntoma); suite de 7 casos al 100% PASS.
- **Pruebas:** `.venv\Scripts\python.exe pruebas.py` → 7/7 PASS (100%); `main.py` validado.
- **Commits:** Pendiente (Entregable 2 completo y robusto).
- **Tiempo:** ~1.7 h
- **Correcciones humanas a la IA:** Corrección de flujo de Streamlit (`StreamlitWidgetAlreadyInstantiatedError`) mediante callbacks y control de lista vacía en recomendación.
- **Siguiente:** Grabación o demostración de DiagnostiPC.

---

### Sesión 2 · 2026-10-21 · F4-05

- **Persona / agente:** Pareja / Antigravity AI
- **Hecho:** Sincronización y actualización integral de los 6 archivos README del repositorio (README.md, docs/adr/, docs/ai/, docs/architecture/, docs/entregables/, docs/product/), alineándolos con la implementación real y los entregables concluidos.
- **Pruebas:** py pruebas.py → 5/5 PASS; swipl consult compilación limpia sin advertencias.
- **Commits:** Pendiente (sincronización de READMEs y documentación).
- **Tiempo:** ~0.3 h
- **Correcciones humanas a la IA:** Ninguna.
- **Siguiente:** Ensayo de sustentación y empaquetado final (F4-06).

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
