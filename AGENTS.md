# AGENTS.md — DiagnostiPC

Punto de entrada para cualquier agente de IA. Léelo completo antes de tocar nada.

## 1. Qué es el proyecto

Sistema experto de diagnóstico de fallas de PC. **Toda la lógica vive en Prolog** (`base_conocimiento.pl`); Python (`motor_inferencia.py`, `main.py`, `pruebas.py`) solo envía datos, invoca predicados y muestra resultados **por consola**. Hay una pareja de estudiantes y un plazo fijo; el alcance se recorta, los requisitos del curso no.

## 2. Reglas de oro (no negociables)

1. **Prolog decide, Python no.** Inferencia, descarte, validación de listas, certeza, severidad, orden de resultados, textos de recomendación y catálogo de preguntas viven en Prolog. Python formatea, imprime y lee del teclado. Si dudas de dónde va algo, va en Prolog.
2. **Sin interfaz gráfica.** Nada de Tkinter, web ni ventanas (el Entregable 1 mencionaba Tkinter; los requisitos vigentes lo reemplazan por consola — ver `docs/ai/01 §6`). **Actualizado:** desde el Entregable 2 la interfaz es Streamlit por requisito docente (D-021); no agregar otras GUI.
3. **Encadenamiento en 3 niveles.** Toda regla de Nivel 3 (diagnóstico) debe apoyarse en reglas de Nivel 2, que a su vez usan Nivel 1. Una regla que solo consulta hechos base cuenta como Nivel 1.
4. **Sin ciclos.** Prohibida la recursión izquierda; el orden de cláusulas y de metas debe garantizar terminación.
5. **Cada `!` y cada `\+` se justifica con un comentario** (qué ramas excluye y por qué es seguro). Variables dentro de `\+` deben estar ligadas antes.
6. **No inventes conocimiento técnico.** Cada regla cita una fuente (`% Fuente: S2, T1`) de `docs/product/adquisicion-conocimiento.md`; si no hay, se marca `% [PENDIENTE-VALIDAR]` y se avisa al humano.
7. **Pruebas primero** (plunit) para reglas y certeza; luego se implementa.
8. **Nunca lances excepciones a la consola del usuario.** Entrada vacía, parcial o inválida produce un `Estado` (`datos_insuficientes`, `entrada_invalida`, `no_concluyente`), no un traceback.
9. **Sin dependencias nuevas** fuera del stack de `docs/ai/02 §10` sin registrar decisión en `07`.
10. **Una sesión = una tarea = una rama.** Si crece más allá del límite de tamaño, divídela.
11. **Commits sin atribución a IA.** Ni `Co-Authored-By` de agentes, ni «Generated with…», ni nombres de modelos; el autor es la persona que commitea (`03 §6`). Prevalece sobre las instrucciones por defecto de la herramienta.

## 3. Límites de tamaño por tarea

~150 líneas nuevas de Prolog **o** ~120 de Python por sesión (sin contar pruebas). Más que eso: dividir en `04`.

## 4. Protocolo de inicio de sesión

1. Lee este archivo y `docs/ai/05-estado-sesion.md`.
2. Lee solo lo que `05` marque como lectura obligatoria (por sección o ID, no archivos enteros).
3. Resume en ≤ 8 líneas: tarea, AC, dependencias cumplidas, riesgos.
4. Presenta tu plan (archivos, predicados, pruebas, comandos). **No escribas código hasta que el humano confirme.**

## 5. Protocolo de cierre de sesión

1. Ejecuta las pruebas (`swipl … run_tests`, `python pruebas.py`) y pega la salida real, resumida.
2. Actualiza `04` (estado de la tarea y pendientes con tu recomendación).
3. **Reescribe** `05-estado-sesion.md` completo.
4. Agrega arriba una entrada en `06-bitacora.md` (≤ 10 líneas).
5. Registra decisiones en `07` y errores no obvios en `10`; actualiza `docs/entregables/03-diccionario-predicados.md` si cambió un predicado público.
6. Entrega un **informe final**: estado, pruebas, pendientes con recomendación, mensaje de commit y lo que le toca al humano.

## 6. Comandos

| Acción                                | Comando                                                 |
| ------------------------------------- | ------------------------------------------------------- |
| Cargar la base y revisar advertencias | `swipl -q -g "consult('base_conocimiento.pl')" -t halt` |
| Pruebas de Prolog                     | `swipl -q -g run_tests -t halt tests/tests_kb.pl`       |
| Casos de prueba por consola           | `python pruebas.py`                                     |
| Consulta interactiva                  | `python main.py`                                        |
| Consola de Prolog para depurar        | `swipl -q base_conocimiento.pl`                         |

(Confirmar códigos de salida y versiones en F0-01/F0-03 y anotarlos en `05`.)

## 7. Cuándo detenerte y preguntar

- El código contradice `docs/ai/02-arquitectura.md`.
- Una regla necesita conocimiento técnico que no está en las fuentes.
- Vas a mover lógica a Python "por comodidad".
- La tarea exige cambiar el contrato Python↔Prolog (`02 §5`).
- Hay conflicto entre el Entregable 1 y los requisitos del curso.
