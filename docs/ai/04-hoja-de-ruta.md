# 04 · Hoja de ruta y tablero de tareas

> Lista maestra de tareas. Cada sesión con un agente trabaja **una** tarea de aquí (≈ 2–3 h).
> Estados: `[ ]` pendiente · `[~]` en curso · `[x]` terminada · `[!]` bloqueada (anotar motivo).
> Formato: **ID** · título — _AC:_ criterio de aceptación — _Dep:_ dependencias — _Resp.:_ responsable sugerido.
> Responsables: **K** = Integrante A (Ingeniero del Conocimiento y Motor Simbólico) · **I** = Integrante B (Ingeniero de Integración y Explicabilidad) · **K+I** = ambos.

---

## F6 · Entregable 3 — DCG en Prolog, Modo Experto en Caliente y Pre-procesamiento Numérico

- [x] **F6-01** · Gramática de Cláusulas Definidas (DCG) en Prolog — Predicado `extraer_sintomas_dcg/2`, lexicón de frases compuestas, sinónimos técnicos y filtrado de ruido/conectores. — _AC:_ Extracción exacta de síntomas canónicos desde secuencias de átomos. — _Resp.:_ K
- [x] **F6-02** · Adquisición Dinámica y Persistencia en Prolog — Predicados dinámicos `:- dynamic`, predicado `registrar_diagnostico_dinamico/5` y persistencia estructurada al final de `base_conocimiento.pl`. — _AC:_ Inyección en memoria viva vía `assertz/1` y supervivencia tras reinicio. — _Resp.:_ K
- [x] **F6-03** · Pre-procesador Numérico Híbrido (`preprocesador_numerico.py`) — Discretización continua de telemetría de PC (temperaturas, voltajes, FPS, latencias) mediante heurística estándar ATX y clasificador Scikit-learn (`DecisionTreeClassifier`). — _AC:_ Discretización determinista a hechos simbólicos. — _Resp.:_ I
- [x] **F6-04** · Adaptación del Puente PySwip en `motor_inferencia.py` — Métodos `procesar_texto_libre()`, `adquirir_nuevo_diagnostico()`, `obtener_diagnosticos_registrados()` y `discretizar_telemetria()`. — _AC:_ Tokenización y serialización segura sin excepciones. — _Resp.:_ I
- [x] **F6-05** · Interfaz Interactiva Evolucionada en `main.py` — Expansores de entrada por lenguaje natural (DCG) y telemetría de sensores; pestaña dedicada "Modo Experto (Adquisición Dinámica)". — _AC:_ Operatividad 100% en Streamlit. — _Resp.:_ I
- [x] **F6-06** · Ampliación de Suite de Pruebas en `pruebas.py` — Casos 8 (DCG), 9 (assertz en memoria), 10 (persistencia .pl) y 11 (telemetría ML). — _AC:_ 11/11 casos en estado PASS (100%). — _Resp.:_ I
- [x] **F6-07** · Sincronización de Documentación Técnica — Actualización de `requirements.txt`, `README.md`, `03-diccionario-predicados.md`, `07-decisiones.md` y bitácoras. — _AC:_ Documentación sincronizada. — _Resp.:_ K+I

---

## F5 · Entregable 2 — Puente PySwip y Motor de Explicabilidad ("Caja Blanca")

- [x] **F5-01** · Motor Simbólico de Explicabilidad en Prolog — Predicados `hechos_comprobados/3`, `regla_disparada/4`, `reglas_disparadas/3` e `hipotesis_descartada/4` (`\+` y falta de evidencia). — _AC:_ Traza exacta en 3 niveles N1 $\to$ N2 $\to$ N3. — _Resp.:_ K
- [x] **F5-02** · Módulo de Recomendación y Desempate en Prolog — Predicados `hipotesis_parcial/5`, `hipotesis_parciales/2`, `peso_sintoma_candidato/4` y `sintoma_desempate/4`. — _AC:_ Cálculo de pesos por criticidad y severidad; desempate determinista sin ciclos. — _Resp.:_ K
- [x] **F5-03** · Puente Python en `motor_inferencia.py` — Métodos `explicar_diagnostico()`, `obtener_hipotesis_descartadas()`, `obtener_hipotesis_parciales()`, `recomendar_siguiente_sintoma()`, `obtener_catalogo_sintomas()` y `obtener_sintomas_por_componente()`. — _AC:_ Tipado y parsing robusto de respuestas PySwip sin excepciones. — _Resp.:_ I
- [x] **F5-04** · Interfaz Interactiva de Usuario en `main.py` — Implementación en Streamlit con multiselect, presets Caso 1 y Caso 2, badges de severidad, panel "¿Por qué?" desplegable y panel "¿Qué falta?" con botón de desempate en un clic. — _AC:_ `streamlit run main.py` y `python main.py` operativos. — _Resp.:_ I
- [x] **F5-05** · Suite de Pruebas Automatizadas en `pruebas.py` — 7 casos cubriendo diagnóstico único, múltiple, exclusión, bordes, trazabilidad "¿Por qué?" y desempate "¿Qué falta?". — _AC:_ 7/7 casos en estado PASS (100%). — _Resp.:_ I
- [x] **F5-06** · Documentación técnica y Diccionario de Predicados — Actualización de `docs/entregables/03-diccionario-predicados.md`, `README.md` y `requirements.txt`. — _AC:_ Documentación sincronizada con el código fuente. — _Resp.:_ K+I

---

## F4 · Documentación y entrega previa (Entregable 1)

- [x] **F4-01** · Diccionario de predicados base. — _Resp.:_ K
- [x] **F4-03** · Evidencia de pruebas del motor. — _Resp.:_ I
- [x] **F4-04** · Ficha de definición y matriz de cumplimiento del Entregable 1. — _Resp.:_ K+I
- [x] **F4-05** · Revisión cruzada de la base de conocimiento y puente. — _Resp.:_ K+I

---

## Pendientes descubiertos (fuera de tarea)

- [ ] **F5-07** · Grabación de la video-demostración de 3 a 5 minutos (o ensayo en vivo) cubriendo Caso 1 (Inferencia completa y "¿Por qué?") y Caso 2 (Evidencia incompleta y "¿Qué falta?"). — _Recomendación:_ Realizar por el equipo humano utilizando los presets de `main.py`.
