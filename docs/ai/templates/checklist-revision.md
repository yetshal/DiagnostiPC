# Checklist de revisión de una tarea (para la otra persona de la pareja)

Marca cada punto al revisar el diff. Un ❌ bloquea el merge.

## Alcance

- [ ] El cambio corresponde a **una** tarea de `04` y su AC se cumple.
- [ ] No hay cambios ajenos a la tarea (renombres, formato masivo).
- [ ] Tamaño dentro del límite (~150 líneas de Prolog o ~120 de Python).

## Límite Prolog / Python

- [ ] Toda lógica de dominio (inferencia, descarte, validación, certeza, severidad, orden) está en Prolog.
- [ ] Python no contiene síntomas, umbrales ni textos de recomendación.
- [ ] La frontera usa solo listas, átomos y enteros.
- [ ] La base no imprime nada.

## Prolog

- [ ] Hechos del mismo predicado contiguos; secciones con encabezado y propósito.
- [ ] Cada regla nueva cita fuente (`S?`/`T?`) o está `[PENDIENTE-VALIDAR]`.
- [ ] Niveles respetados: N3 → N2 → N1 → hechos; sin llamadas ascendentes ni recursión izquierda.
- [ ] Cada `!` tiene `% CORTE:` (qué descarta y por qué es seguro).
- [ ] Cada `\+` tiene `% NEGACION:` y sus variables están ligadas antes.
- [ ] Se usan listas donde corresponde (`member`, conteo, filtrado, pliegue de FC).
- [ ] La recolección usa `findall`/`setof`/`bagof` y no devuelve duplicados.
- [ ] Sin variables _singleton_; carga sin advertencias.
- [ ] Identificadores de regla (`rNN`) únicos.

## Certeza y severidad

- [ ] FC enteros 0–100; combinación con la fórmula de ADR-005.
- [ ] Umbrales 19/20, 39/40, 69/70 probados.
- [ ] Severidad entre 1 y 4; precedencias por cortes probadas.
- [ ] El orden de resultados es total y determinista.

## Python

- [ ] `try/except` solo en `motor_inferencia.py` y en el bucle de `main.py`.
- [ ] Consultas consumidas o cerradas; sin generadores huérfanos.
- [ ] Entrada del usuario validada contra las opciones ofrecidas; sin `eval`/`exec`.
- [ ] Lista vacía, parcial o inválida **no** produce traceback.

## Pruebas

- [ ] plunit: caso positivo y negativo por cada predicado nuevo.
- [ ] `swipl -q -g run_tests -t halt tests/tests_kb.pl` pasa (salida real vista).
- [ ] `python pruebas.py` pasa si la tarea toca la frontera.
- [ ] Casos de borde: lista vacía, un solo síntoma, valores en los umbrales.

## Documentación

- [ ] `04` (estado), `05` (reescrito) y `06` (entrada nueva) actualizados.
- [ ] `entregables/03-diccionario-predicados.md` al día si cambió un predicado público.
- [ ] `07`/`08`/`10` actualizados si hubo decisión, término nuevo o error no obvio.

## Git

- [ ] Rama `feat|fix|docs|test/Fx-NN-…`; commits convencionales en español.
- [ ] Sin archivos temporales ni secretos.

## Entendimiento

- [ ] Puedo explicar en 2 minutos qué hace el cambio, por qué cada corte/negación es seguro y a qué nivel pertenece cada regla.
