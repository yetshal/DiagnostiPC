# 03 · Pautas de programación

> Reglas concretas para escribir código en DiagnostiPC. Un agente debe cumplirlas sin que se le recuerden. Si una regla impide algo razonable, pregunta antes de saltártela.

## 1. Forma de trabajar del agente

1. **Entiende antes de escribir:** lee tu tarea en `04`, su AC y las secciones de `02` que cite.
2. **Plan corto primero:** predicados a crear, pruebas a escribir, archivos que tocas.
3. **Pruebas primero** (plunit): para certeza, severidad y cada regla, escribe los casos positivo y negativo antes de la regla.
4. **De abajo hacia arriba:** hechos → utilidades de listas → Nivel 1 → Nivel 2 → Nivel 3 → certeza/severidad → API pública → puente Python → consola.
5. **Ejecuta y lee la salida real** de `swipl` y `python`. Nunca digas "debería funcionar".
6. **Sin código muerto ni TODOs huérfanos:** `% TODO(F2-05): …`.
7. **No reformatees lo que no tocas.**
8. **Conocimiento técnico dudoso → pregunta.** No rellenes con lo que "suena razonable" de hardware (ver §2).
9. **Cambios que no convienen ahora:** no los hagas en silencio ni los descartes sin avisar: qué es, por qué no ahora y tu recomendación; regístralo en `04 §Pendientes`.
10. **Se recorta alcance, no requisitos del curso.**

## 2. Conocimiento del dominio (la parte que más se equivoca)

- Cada regla N3 lleva un comentario `% Fuente: S?, T?` con IDs de `docs/product/adquisicion-conocimiento.md`.
- Los FC de cada regla y los umbrales (antigüedad, meses sin limpieza, RAM mínima) son **propuestas** hasta que el técnico las valide; marca `% [PENDIENTE-VALIDAR]`.
- Los textos de recomendación vienen de la tabla del Entregable 1 (Tabla 3) o de una fuente; no los reescribas con consejos nuevos.
- Una regla que "se parece mucho" a otra se **fusiona o se justifica**, no se duplica.

## 3. Prolog

### 3.1. Estilo

- Una cláusula por línea de cabeza; metas del cuerpo en líneas separadas con 4 espacios de sangría; `,` al final de cada meta; punto en la última.
- Encabezado de sección:

```prolog
%% ===========================================================================
%% SECCIÓN 6 · NIVEL 2 — Categorías e indicios (usa solo predicados de Nivel 1)
%% ===========================================================================
```

- Antes de cada predicado, un comentario de una o dos líneas: qué comprueba y modo de uso (`%! predicado(+Entrada, -Salida)`).
- Hechos de un mismo predicado **siempre contiguos**; sin `discontiguous`.
- Variables en `CamelCase`, anónimas con `_`; ninguna variable "singleton" (la carga no debe emitir advertencias).
- Líneas ≤ 100 columnas. Sin tabuladores.

### 3.2. Niveles y dependencias

- **N1** solo consulta la lista (`respuesta/3`) y hechos de catálogo.
- **N2** solo llama a N1 y a hechos.
- **N3** llama a N2 y N1; nunca a otro N3 ni a sí mismo.
- Prohibido que un predicado de nivel inferior llame a uno superior.
- Orden de metas: primero las más restrictivas y baratas (condiciones sobre la lista), después las que enumeran.

### 3.3. Corte `!`

- Solo en tres usos: (a) **exclusión mutua** (umbrales, precedencia de ajustes), (b) **cláusula por defecto** (fallback) y (c) **determinismo** tras una prueba que ya decidió.
- El corte va **después** de las condiciones que identifican el caso, nunca antes.
- Cada `!` tiene un comentario `% CORTE: …` que dice qué ramas descarta y por qué es seguro. Un corte sin comentario no se acepta.
- Si quitar el corte cambia el resultado de las pruebas, es un corte "rojo": justifícalo con una prueba que lo demuestre.

### 3.4. Negación `\+`

- Todas las variables dentro de `\+` deben estar **ligadas** antes de evaluarla (pon la meta que las liga a la izquierda).
- Comentario `% NEGACION: …` indicando la condición excluyente.
- No uses `\+` como sustituto de un `!` por pereza.

### 3.5. Listas y recolección

- Listas siempre `Var-Valor` en la frontera; usa `member/2`, `memberchk/2`, `length/2`, `subtract/3`, `exclude/3`, `include/3`, `sort/2`, `msort/2`, `sumlist`/`sum_list` según convenga.
- Para recolectar: `findall/3` (devuelve `[]` si no hay soluciones). Si usas `bagof/setof`, declara variables libres con `^`; recuerda que **fallan** si no hay soluciones.
- Deduplicar con `sort/2` o `setof/3`; ordenar con `sort/4` o `predsort/3` con comparador **total** (ver `10` T-07).

### 3.6. Ciclos

- Nada de reglas que se llamen a sí mismas por la izquierda. Si necesitas recursión (pliegue de FC, conteo), recorre la lista con la cola decreciente y caso base `[]` primero.
- Antes de cerrar cualquier tarea de reglas: ejecuta `trace` o consultas de prueba con entradas "raras" para confirmar terminación (RNF-03).

### 3.7. Salidas

- La base **no imprime**. Sin `format/2`, `write/1`, `print_message/2` para datos del usuario.

## 4. Python

### 4.1. Estilo

- Python 3.11+, tipos en firmas, `from __future__ import annotations` opcional.
- Nombres en español `snake_case` (coherente con el dominio): `cargar_base`, `diagnosticar`.
- Docstrings cortos en español: qué hace, qué recibe, qué devuelve.
- Sin globales mutables; el motor Prolog se encapsula en una clase o módulo con funciones `cargar_base()`, `consultar()`, `cerrar()`.

### 4.2. Qué sí y qué no hace Python

| Sí                                                                                            | No                                                        |
| --------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| Cargar el `.pl` y verificar que los predicados públicos existen                               | Decidir si un síntoma "cuenta"                            |
| Construir el texto de la consulta con átomos validados                                        | Ordenar, filtrar o deduplicar resultados                  |
| Leer del teclado y mapear número de opción → átomo de la lista de opciones que Prolog entregó | Calcular certeza o severidad                              |
| Formatear e imprimir tablas                                                                   | Escribir textos de recomendación o preguntas              |
| Capturar excepciones del puente y mostrar mensajes claros                                     | Interpretar `Estado` con reglas propias (solo lo imprime) |

### 4.3. Robustez

- Entrada de usuario: validar que la opción exista en las ofrecidas; si no, volver a preguntar. No usar `eval`/`exec`.
- Cerrar las consultas abiertas; no dejar generadores sin consumir.
- `try/except` solo en `motor_inferencia.py` y en el bucle principal de `main.py`.

## 5. Pruebas

| Tipo                | Herramienta  | Qué cubre                                                                              | Cuándo         |
| ------------------- | ------------ | -------------------------------------------------------------------------------------- | -------------- |
| Catálogo            | plunit       | Cada variable tiene pregunta y valores; sin duplicados; 38 variables y 10 diagnósticos | F1             |
| Unitarias de reglas | plunit       | Cada predicado N1/N2/N3: caso verdadero y caso falso                                   | Con cada regla |
| Certeza y severidad | plunit       | Bordes de umbral (19/20, 39/40, 69/70); límites 1 y 4; precedencias                    | F2-01, F2-07   |
| Integración Prolog  | plunit       | `diagnosticar_todos/3` con los casos del plan                                          | F2-08          |
| Consola             | `pruebas.py` | Los 5+ casos del entregable; salida formateada                                         | F3-03          |
| Cumplimiento        | plunit (S)   | Conteo de hechos y reglas; presencia de `!`, `\+`, `findall`                           | F4-02          |

- Nombres descriptivos: `test(pitidos_largos_sin_imagen_diagnostica_ram)`.
- Un bug corregido = una prueba que falla antes y pasa después.
- Las pruebas no dependen del orden ni de estado global.

## 6. Git

- Rama por tarea: `feat/F2-04-diagnosticos-arranque`, `fix/…`, `docs/…`.
- Commits convencionales, en español: `feat(kb): agregar reglas de arranque`.
- Un commit lógico por cambio; el PR menciona el ID de tarea y lo revisa **la otra persona de la pareja**.
- `main` solo recibe PR con pruebas pasando.
- El agente hace `push` solo si se lo piden.

## 7. Lista de verificación por cambio

- [ ] ¿La lógica nueva está en Prolog? ¿Hay algo de dominio en Python?
- [ ] ¿Cada regla nueva cita fuente o está `[PENDIENTE-VALIDAR]`?
- [ ] ¿Cada `!` tiene `% CORTE:` y cada `\+` tiene `% NEGACION:` con variables ligadas?
- [ ] ¿Respeta N3 → N2 → N1? ¿Sin recursión izquierda?
- [ ] ¿La carga de `base_conocimiento.pl` sale sin advertencias?
- [ ] ¿Entrada vacía o inválida produce `Estado`, no excepción?
- [ ] ¿El diccionario de predicados refleja el cambio?
- [ ] ¿Dependencia nueva? Requiere decisión en `07`.

## 8. Definición de terminado (DoD)

1. Cumple su **AC** con evidencia (salida de pruebas).
2. `swipl … run_tests` y, si tocó la frontera, `python pruebas.py` pasan; carga sin advertencias.
3. Comentarios obligatorios presentes (sección, propósito, fuente, CORTE, NEGACION).
4. Sin `print`/`write` de depuración ni código comentado.
5. Docs al día: `04`, `05`, `06`; `02`/`07`/`08`/`10` y `entregables/03` si aplica.
6. Revisado por la otra persona con `templates/checklist-revision.md`.

## 9. Antipatrones prohibidos

- Poner `if/else` de dominio en Python ("si hay pitidos largos entonces…").
- Ordenar o filtrar los resultados en Python.
- Hechos dinámicos (`assert`/`retract`) para guardar respuestas.
- Reglas de N3 que consultan solo `respuesta/3` (se saltan N1 y N2).
- Cortes sin comentario o puestos "hasta que dé el resultado".
- `\+` con variables sin ligar.
- Constantes de dominio (`"enciende"`, umbrales) repetidas en `.py`.
- "Arreglar" una prueba cambiando el esperado para que coincida con un bug.
- Inventar síntomas, FC o recomendaciones sin fuente.
- Copiar y pegar reglas casi idénticas en lugar de parametrizar con un hecho.
