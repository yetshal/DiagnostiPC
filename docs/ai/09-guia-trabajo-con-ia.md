# 09 · Guía para trabajar en pareja con agentes de IA

> Este archivo es para ustedes, no para el agente. Explica cómo sacarle provecho a los agentes en un proyecto académico en pareja sin perder el control, la calidad ni la capacidad de sustentar.

## 1. Ritmo recomendado

- **1 sesión por día** (2–3 h) o dos en paralelo (una persona en Prolog y otra en Python cuando las tareas no dependan entre sí: F0-02/F0-03, F1-02/F3-01 con base mínima, etc.).
- **Al inicio de cada sesión (10 min):** lean `05`, decidan la tarea y quién la conduce.
- **Una vez por fase (20 min):** retro corta: ¿vamos en fecha?, ¿pendientes?, ¿aplicamos la regla de recorte?
- **Compuerta F2:** punto de decisión de recorte. Lleguen a ella con los 5 casos pasando en plunit.

## 2. Ciclo de una sesión

1. **Antes:** revisen `05`. Si la tarea es grande, divídanla en `04`.
2. **Inicio:** `templates/prompt-inicio-sesion.md` (con Claude Code basta "inicia la sesión").
3. **Plan:** exijan el plan (predicados, pruebas, archivos) antes del código. Corregirlo ahí es lo más barato.
4. **Ejecución:** dejen trabajar; interrumpan si el agente pone lógica en Python, inventa síntomas, usa `assert` o añade dependencias.
5. **Revisión (la otra persona):** `templates/checklist-revision.md`. Ejecuten ustedes mismos `run_tests` y `pruebas.py` al menos una vez por sesión.
6. **Cierre:** `templates/prompt-cierre-sesion.md`. Verifiquen que se actualizaron `04`, `05`, `06` y el diccionario.
   - **Verificación opcional pero recomendada** en F2-07, F2-08 y F4-05: `templates/prompt-verificacion-sesion.md`.
7. **Commit y PR:** la otra persona aprueba; fusionen con las pruebas en verde.

## 3. Reglas prácticas

- **Una sesión = una tarea = una rama = un PR.** Sesiones largas degradan el contexto del agente.
- **La IA propone reglas; el técnico y las fuentes las validan.** El mayor riesgo de este proyecto no es el código sino el **conocimiento inventado**: un agente produce reglas de hardware que suenan bien y pueden estar mal. Exijan siempre la fuente (`S?`/`T?`) o la marca `[PENDIENTE-VALIDAR]`.
- **Los FC y los umbrales son números de criterio, no de la IA.** Se acuerdan con el técnico (F1-05, F2-11).
- **Desconfíen de "ya funciona".** Pidan la salida real de `swipl` y de `python pruebas.py`.
- **Entiendan lo que entregan.** Si no pueden explicar un corte, una negación o por qué una regla es N2 y no N3, pidan que se la expliquen **antes** de aceptarla: tendrán que sustentarla (F4-06).
- **Empiecen una sesión nueva** si el agente repite errores, mete lógica en Python o la conversación se alarga; antes, que cierre la sesión correctamente.
- **Revisión doble** en: certeza (F2-01), severidad (F2-07), recolección y estados (F2-08), puente (F3-01).
- **Si una tarea se atrasa más de medio día:** apliquen la regla de recorte o dividan la tarea.
- **Uso de IA:** si la asignatura exige declarar el uso de IA, la bitácora (`06`) ya registra qué se hizo con apoyo de agentes y qué correcciones humanas hubo.

## 4. Prompts útiles

**Planificar una tarea grande**

> Lee F2-04 en `04-hoja-de-ruta.md` y `02 §6–§7`. No escribas código. Lista los predicados de Nivel 3 que necesito para DX01, DX02 y DX05, de qué predicados de N2/N1 dependen y qué casos de prueba positivos y negativos propones. Marca lo que necesite validación del técnico.

**Pruebas primero**

> Para F2-01 escribe solo las pruebas plunit de `combinar_certeza/3` y `nivel_certeza/2` con los bordes 19/20, 39/40, 69/70, y muéstrame la lista de casos antes de implementar.

**Auditoría de cortes y negaciones**

> Revisa `base_conocimiento.pl`. Para cada `!` dime qué ramas descarta y si es un corte rojo; para cada `\+`, si sus variables están ligadas. Señala cortes sin comentario. No cambies nada todavía.

**Auditoría de ciclos y niveles**

> Construye el grafo de llamadas entre predicados de las secciones 5–9 y verifica que va solo de N3 a N2 a N1. Lista cualquier llamada ascendente o recursiva.

**Auditoría del límite Prolog/Python**

> Revisa `motor_inferencia.py`, `main.py` y `pruebas.py`. Enumera cualquier `if` o constante que represente conocimiento del dominio (síntomas, umbrales, textos de recomendación). No cambies nada todavía.

**Depurar sin dar vueltas**

> Antes de proponer cambios, revisa `10-errores-conocidos.md`. Luego reproduce el error con una consulta mínima en `swipl` y solo después corrígelo.

**Redactar la ficha o el diccionario**

> Lee `base_conocimiento.pl` y genera una fila del diccionario por predicado público (firma, modo, descripción, ejemplo de invocación desde Python). Marca cuáles no existen en el archivo.

## 5. Qué evita que el plazo se rompa

1. **Recortar alcance Should/Could, no requisitos del curso** (regla de `04`).
2. **Tener el puente funcionando desde S2** (F0-02): es el mayor riesgo técnico.
3. **Los 5 casos de prueba escritos desde F2:** guían las reglas y evitan el pánico de la última semana.
4. **Reunirse pronto con el técnico:** sin su validación, las reglas son hipótesis.
5. **Revisión cruzada continua:** que cada persona entienda toda la base, no solo su parte.

## 6. Registro del proceso

`06-bitacora.md` guarda sesiones, tiempos reales y correcciones humanas. En F4-07 permite responder: ¿cuánto tardó cada tarea frente a lo estimado?, ¿qué errores cometió la IA con más frecuencia (conocimiento, cortes, ciclos, lógica en Python)?

## 7. Herramientas

- **Claude Code:** lee `CLAUDE.md` automáticamente.
- **Codex, Cursor, Copilot, Gemini CLI y otros:** la mayoría lee `AGENTS.md`; si alguno no, pegue el prompt de inicio.
- El traspaso vive en los archivos (`05`), así que pueden alternar agentes.
- **Útil en la depuración:** `swipl` interactivo con `trace/0`, `listing/1` y `explain/1`; plunit con `run_tests/1` para correr una sola suite.
