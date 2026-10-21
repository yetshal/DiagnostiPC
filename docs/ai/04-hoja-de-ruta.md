# 04 · Hoja de ruta y tablero de tareas

> Lista maestra de tareas. Cada sesión con un agente trabaja **una** tarea de aquí (≈ 2–3 h).
> Estados: `[ ]` pendiente · `[~]` en curso · `[x]` terminada · `[!]` bloqueada (anotar motivo).
> Formato: **ID** · título — _AC:_ criterio de aceptación — _Dep:_ dependencias — _Resp.:_ responsable sugerido.
> Responsables (roles del Entregable 1): **K** = Líder de Conocimiento y Modelado Lógico (Prolog) · **I** = Líder de Integración e Interfaz (Python) · **K+I** = ambos. Ajusta nombres en `05`.
> Tareas marcadas _(no código)_ las hace el equipo, no el agente.
> **Fechas:** la fecha de entrega está por definir (pregunta abierta en `05`). El plan se mide en **sesiones (S)** de 2–3 h; con una sesión diaria ≈ 15 días, con dos personas en paralelo puede comprimirse.

## Resumen de fases

| Fase                         | Sesiones | Objetivo                                                                    | Compuerta                                                                                            |
| ---------------------------- | -------- | --------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| F0 · Preparación             | S1–S2    | Entorno, puente probado, plunit funcionando, dudas con el docente resueltas | Una consulta Python→Prolog devuelve una lista; `run_tests` corre; respuestas del docente anotadas    |
| F1 · Conocimiento y hechos   | S3–S5    | Tabla de conocimiento con fuentes, catálogos y validación de entrada        | ≥ 30 hechos (meta ≈ 110) con pruebas; validación de listas sin excepciones                           |
| F2 · Motor lógico            | S6–S10   | N1, N2, N3, certeza, severidad, recolección, estados                        | Los 5 casos pasan en plunit; ≥ 15 reglas (meta ≥ 40 cláusulas); cero ciclos; **decisión de recorte** |
| F3 · Integración en consola  | S11–S13  | Puente, `main.py`, `pruebas.py`                                             | `python pruebas.py` muestra ≥ 5 casos formateados con obtenido = esperado                            |
| F4 · Documentación y entrega | S14–S15  | Diccionario, evidencia, ficha, matriz al 100 %, paquete                     | Matriz de cumplimiento completa; reproducción en 2.ª máquina                                         |

### Regla de recorte (si vas atrasado)

Si al cierre de F2 hay **más de 1 sesión de retraso**, se recorta en este orden, sin discusión: **1)** F3-04 preguntas dinámicas (RF-20) · **2)** F2-09 explicación (RF-18) · **3)** F4-02 prueba automática de mínimos (se hace la verificación manual de la matriz) · **4)** meta de 40 cláusulas-regla baja a ≥ 24 (nunca por debajo de 15 ni de los tres niveles) · **5)** último recurso: reducir diagnósticos de 10 a 8 (se omiten DX09 y DX10) **y se actualiza la ficha**.

**Nunca se recortan:** los tres niveles encadenados, listas, `!`, `\+`, `findall`, severidad, los 5 casos de prueba, el diccionario, la ficha y la lógica 100 % en Prolog.

---

## F0 · Preparación (S1–S2)

- [x] **F0-00** · Documentación base (`AGENTS.md`, `docs/ai/`, ADR 001–006, entregables, producto). — _AC:_ paquete revisado por la pareja. — _Dep:_ — _Resp.:_ K+I
- [ ] **F0-01** · Entorno y repositorio — instalar SWI-Prolog y Python, crear repositorio con la estructura de `02 §3`, `.gitignore`, `requirements.txt` (solo el puente), README con comandos. Anotar versiones reales en `05`. — _AC:_ `swipl --version` y `python --version` funcionan en **ambas** máquinas; repositorio clonado por los dos. — _Dep:_ F0-00 — _Resp.:_ K+I
- [ ] **F0-02** · Spike del puente — `base_conocimiento.pl` mínimo (un hecho y una regla que reciben una lista y devuelven otra con `findall`) y `motor_inferencia.py` con `cargar_base()`/`consultar()`. Probar: lista de entrada, lista de salida, texto con tildes, consulta que falla, consulta sin resultados y cierre de consultas. Si PySwip falla, probar Janus y registrar la decisión en ADR-002. — _AC:_ Python imprime la lista devuelta por Prolog para una entrada de 3 elementos; una consulta sin solución no lanza excepción; decisión de puente anotada en `07`. — _Dep:_ F0-01 — _Resp.:_ I
- [ ] **F0-03** · plunit funcionando — `tests/tests_kb.pl` con una prueba trivial que carga `base_conocimiento.pl`; documentar el comando y su código de salida cuando una prueba falla. — _AC:_ `swipl -q -g run_tests -t halt tests/tests_kb.pl` pasa; al romper una prueba a propósito, el código de salida es distinto de 0 (anotar resultado real en `05`). — _Dep:_ F0-01 — _Resp.:_ K
- [ ] **F0-04** · _(no código)_ Acuerdos y confirmaciones — roles, flujo de ramas y revisión cruzada, fecha de entrega. **Preguntar al docente:** (a) ¿se acepta consola en lugar de Tkinter? (b) ¿nombre del módulo `motor.py` o `motor_inferencia.py`? (c) ¿PySwip o Janus? (d) ¿el Entregable 1 con ≥ 40 reglas sigue vigente o aplica el mínimo de 15? (e) ¿formato de entrega (zip, repositorio, PDF)? — _AC:_ respuestas anotadas en `05`; ADR-006 confirmada o ajustada. — _Dep:_ — _Resp.:_ K+I
- [ ] **F0-05** · _(no código)_ Preparar la adquisición de conocimiento — reunir fuentes S1…Sn con ID, agendar la 1.ª reunión con el técnico y llevarle el guion de `docs/product/adquisicion-conocimiento.md`. — _AC:_ ≥ 4 fuentes con ID y cita; fecha de la reunión fijada. — _Dep:_ — _Resp.:_ K

**Compuerta F0:** puente probado en ambas máquinas; plunit corre; respuestas del docente anotadas.

---

## F1 · Conocimiento y hechos (S3–S5)

- [ ] **F1-01** · _(no código)_ Tabla de conocimiento — por cada diagnóstico DX01–DX10: síntomas que lo apoyan (con FC propuesto), condiciones que lo descartan, severidad base, recomendación, fuente. — _AC:_ tabla completa en `docs/product/adquisicion-conocimiento.md §4`; cada fila con fuente o `[PENDIENTE-VALIDAR]`. — _Dep:_ F0-05 — _Resp.:_ K
- [ ] **F1-02** · Catálogo de variables — secciones 1 y 3 del `.pl`: `pregunta/3`, `valor_permitido/2`, `grupo_variable/2` para las 38 variables (A1–G8). Átomos según `08`. — _AC:_ 38 + 38 + 38 hechos contiguos; plunit: toda variable del glosario existe, sin duplicados, cada una con ≥ 2 valores o tipo numérico. — _Dep:_ F0-03 — _Resp.:_ K
- [ ] **F1-03** · Catálogo de diagnósticos y escalas — `diagnostico/2`, `severidad_base/2`, `recomendacion/2` (10 cada uno), `nivel_severidad/3` (4), `umbral_certeza/2` (3). — _AC:_ las severidades base coinciden con la Tabla 3 del Entregable 1; plunit verifica 10 diagnósticos con los 3 datos cada uno. — _Dep:_ F1-01, F0-03 — _Resp.:_ K
- [ ] **F1-04** · Utilidades de listas y validación de entrada — `respuesta/3`, `cumple_todas/2`, `subconjunto/2`, `contar_cumplidas/3`, `filtrar_validas/2`, `validar_entrada/2`. — _AC:_ plunit con: lista vacía, lista con variable desconocida, valor fuera de catálogo, duplicados, lista parcial, lista completa; ninguna lanza excepción. — _Dep:_ F1-02 — _Resp.:_ K
- [ ] **F1-05** · _(no código)_ Sesión 1 con el técnico — validar la tabla de F1-01 (síntomas, descartes, severidades, umbrales de contexto). — _AC:_ observaciones en `adquisicion-conocimiento.md §5`; tabla corregida. — _Dep:_ F1-01 — _Resp.:_ K

**Compuerta F1:** ≥ 30 hechos agrupados en secciones (meta ≈ 110) con pruebas; validación de listas robusta.

---

## F2 · Motor lógico (S6–S10)

- [ ] **F2-01** · Certeza — `combinar_certeza/3`, `combinar_lista/2`, `nivel_certeza/2` (cortes por umbral). — _AC:_ plunit: `80,50 → 90`; lista vacía → 0; un elemento → él mismo; asociatividad en 3 valores; etiquetas en 19/20, 39/40, 69/70, 100. Cada `!` comentado. — _Dep:_ F1-03 — _Resp.:_ K
- [ ] **F2-02** · Nivel 1 — ≥ 10 predicados de condiciones elementales (`equipo_enciende/1`, `sin_imagen/1`, `pitidos_largos/1`, `olor_quemado/1`, `equipo_antiguo/1`, `sin_limpieza_reciente/1`, `sin_respaldo/1`, `usa_hdd/1`, `problema_permanente/1`, `valida_respuesta/1`…). — _AC:_ cada predicado con prueba positiva y negativa; solo consultan la lista y hechos. — _Dep:_ F1-04 — _Resp.:_ K
- [ ] **F2-03** · Nivel 2 — `categoria/2` (energía, arranque, video, rendimiento, almacenamiento, software) e indicios intermedios (`indicio_calor/1`, `indicio_disco/1`, `indicio_malware/1`, `recursos_limitados/1`…) usando solo N1. — _AC:_ el ejemplo del Entregable 1 produce `categoria(R, arranque)`; ≥ 10 predicados N2 con pruebas; sin llamadas a N3. — _Dep:_ F2-02 — _Resp.:_ K
- [ ] **F2-04** · Nivel 3 (a) arranque, energía y video — `evidencia/4` para DX01 fuente de poder, DX02 RAM, DX05 gráfica; exclusión RAM/gráfica con `\+`. — _AC:_ caso del Entregable 1 (pitidos largos + sin imagen + cambio de hardware) da `falla_ram` con FC 90; la gráfica **no** aparece cuando hay pitidos largos; cada regla cita fuente. — _Dep:_ F2-03, F2-01 — _Resp.:_ K
- [ ] **F2-05** · Nivel 3 (b) almacenamiento, calor, CMOS y recursos — DX03, DX04, DX09, DX10. — _AC:_ pruebas ✓/✗ por diagnóstico; DX09 no se dispara si hay síntomas de energía graves (`\+`); ≥ 1 regla por diagnóstico. — _Dep:_ F2-03, F2-01 — _Resp.:_ K
- [ ] **F2-06** · Nivel 3 (c) software — DX06 corrupción de SO/arranque, DX07 malware, DX08 conflicto de controladores. — _AC:_ pruebas ✓/✗; malware vs. actualización defectuosa excluidos mutuamente donde corresponda (con `\+` y/o `!` comentados). — _Dep:_ F2-03, F2-01 — _Resp.:_ K
- [ ] **F2-07** · Severidad ajustada — `severidad_ajustada/3` con los criterios de `02 §7` y límites [1, 4]; precedencia por cortes. — _AC:_ una prueba por criterio; ejemplo del Entregable 1 (alta → media por cambio de hardware); crítica no sube más; baja no baja más; olor a quemado fuerza crítica aunque haya baja ocasional. — _Dep:_ F2-04, F2-05, F2-06 — _Resp.:_ K
- [ ] **F2-08** · Recolección, prioridad y estados — `diagnosticar_todos/3` con `findall`, combinación de FC por diagnóstico, descarte < 20, orden total por (severidad ↓, FC ↓, nombre), y `Estado` por cortes (`entrada_invalida` → `datos_insuficientes` → `no_concluyente` → `ok`). — _AC:_ los 5 casos de `entregables/04` pasan en plunit; el resultado no tiene duplicados; `[]` devuelve `datos_insuficientes`. — _Dep:_ F2-07 — _Resp.:_ K
- [ ] **F2-09** · Explicación (RF-18) — `explicar/3`: ids de reglas disparadas con su FC para un diagnóstico. — _AC:_ para el caso del Entregable 1 devuelve `[r12-80, r13-50]`. — _Dep:_ F2-08 — _Resp.:_ K
- [ ] **F2-10** · Auditoría de ciclos, cortes y negaciones — revisar toda la base con la checklist; confirmar que cada `!`/`\+` tiene comentario, que N3 → N2 → N1, y que la carga no da advertencias. — _AC:_ checklist de `templates/checklist-revision.md` §Prolog firmada por la otra persona; consultas con entradas aleatorias del catálogo (≥ 200) terminan. — _Dep:_ F2-08 — _Resp.:_ K+I
- [ ] **F2-11** · _(no código)_ Sesión 2 con el técnico — validar reglas, FC y severidades con los 5 casos. — _AC:_ observaciones registradas; ajustes críticos entran a F2-04…F2-07 o a pendientes. — _Dep:_ F2-08 — _Resp.:_ K

**Compuerta F2:** 5 casos pasan en plunit; ≥ 15 reglas (meta ≥ 40 cláusulas); sin ciclos; **decisión de recorte**.

---

## F3 · Integración en consola (S11–S13)

- [ ] **F3-01** · `motor_inferencia.py` — `cargar_base()` (verifica predicados públicos), `diagnosticar(respuestas)` → diccionario `{estado, resultados}`, `catalogo()`, `explicar()`, validación de átomos, cierre de consultas y manejo de excepciones. — _AC:_ `diagnosticar([])` devuelve `datos_insuficientes` sin excepción; un `.pl` roto da un mensaje claro; Python sin constantes de dominio. — _Dep:_ F0-02, F2-08 — _Resp.:_ I
- [ ] **F3-02** · `main.py` — cuestionario construido desde `catalogo_preguntas/1`, captura con reintento ante opciones inválidas, tabla de resultados, opción de ver la explicación, salida con Ctrl+C. — _AC:_ el flujo del Entregable 1 se completa a mano y muestra `falla_ram`, FC 90, severidad media, recomendación; ningún traceback ante entradas absurdas. — _Dep:_ F3-01 — _Resp.:_ I
- [ ] **F3-03** · `pruebas.py` — ≥ 5 casos: normal 1, normal 2, exclusión, borde 1, borde 2. Cada uno imprime objetivo, entrada, consulta en Prolog, esperado, obtenido y OK/FALLO; escribe `evidencia/salida_pruebas.txt`; código de salida ≠ 0 si algo falla. — _AC:_ `python pruebas.py` termina con código 0 y la salida contiene los 5 bloques formateados. — _Dep:_ F3-01 — _Resp.:_ I
- [ ] **F3-04** · Preguntas dinámicas (RF-20, C) — `siguiente_pregunta/2` en Prolog y bucle en `main.py` que solo la muestra. — _AC:_ si `enciende-no`, no se pregunta por ventanas emergentes; en el caso del Entregable 1 se llega al diagnóstico con ≤ 8 preguntas. — _Dep:_ F3-02 — _Resp.:_ K+I
- [ ] **F3-05** · Reproducción en entorno limpio — clonar en la otra máquina (o un `venv` nuevo) y seguir solo el README. — _AC:_ `python pruebas.py` pasa en ≤ 15 min; pasos faltantes añadidos al README. — _Dep:_ F3-03 — _Resp.:_ K+I

**Compuerta F3:** `python pruebas.py` con ≥ 5 casos formateados y obtenido = esperado; `main.py` completo; reproducible.

---

## F4 · Documentación y entrega (S14–S15)

- [x] **F4-01** · Diccionario de predicados final — completar `entregables/03` con firma, modo (`+`, `-`, `?`), descripción e invocación desde Python; verificar con `current_predicate/1` que cada predicado listado existe. — _AC:_ 100 % de los predicados públicos y de nivel documentados; ninguno inexistente. — _Dep:_ F3-03 — _Resp.:_ K
- [ ] **F4-02** · Prueba automática de cumplimiento (S) — plunit que cuenta hechos y cláusulas-regla y detecta `!`, `\+`, `findall` y listas en el cuerpo de las cláusulas (`clause/2`). — _AC:_ pasa con ≥ 30 hechos y ≥ 15 reglas y detecta una base sin cortes (prueba negativa). — _Dep:_ F2-10 — _Resp.:_ K
- [x] **F4-03** · Evidencia — ejecutar la suite, guardar salida en `evidencia/`, capturas de `main.py`, completar `entregables/04`. — _AC:_ cada caso con objetivo, entrada, consulta, esperado y obtenido; archivos en el repositorio. — _Dep:_ F3-03 — _Resp.:_ I
- [x] **F4-04** · Ficha final y matriz de cumplimiento — actualizar la ficha con los cambios respecto al Entregable 1 (consola, FC enteros, nº de reglas) y marcar cada requisito en `entregables/02`. — _AC:_ matriz con RF-01…RF-16 en ✅ y evidencia enlazada. — _Dep:_ F4-01, F4-03 — _Resp.:_ K+I
- [x] **F4-05** · Revisión cruzada final — la otra persona revisa todo el `.pl` y los `.py` con la checklist; limpieza de comentarios y de código muerto. — _AC:_ checklist completa; carga sin advertencias; ninguna constante de dominio en `.py`. — _Dep:_ F4-04 — _Resp.:_ K+I
- [ ] **F4-06** · Paquete de entrega y ensayo de sustentación — armar el entregable según el formato del docente; cada integrante explica en 5 min un componente (reglas N1→N3, corte/negación, puente). — _AC:_ paquete verificado desde cero; ambos explican sin leer. — _Dep:_ F4-05 — _Resp.:_ K+I
- [ ] **F4-07** · _(no código)_ Retro y bitácora de uso de IA — qué funcionó, qué corrigieron a la IA, tiempos reales por tarea. — _AC:_ `06-bitacora.md` completa. — _Dep:_ F4-06 — _Resp.:_ K+I

**Compuerta F4:** entrega completa con matriz al 100 %; reproducción verificada; ambos preparados para sustentar.

---

## Pendientes descubiertos (fuera de tarea)

> Agrupados por la tarea donde se resuelven. Formato: `- [ ] descripción — recomendación (hacerlo en Fx-NN / no hacerlo) — origen (sesión N)`.

_(vacío)_
