# ADR-003: Respuestas como lista pasada a los predicados (sin base de hechos dinámica)

- **Estado:** Aceptada
- **Fecha:** 2026-10-21
- **Decisores:** Pareja
- **Tarea relacionada:** F1-04, F2-08

## Contexto y problema

El Entregable 1 describía `respuesta/2` como hechos de la sesión guardados con `assert`. Los requisitos del curso piden, además, **procesar listas** enviadas desde Python (subconjuntos, conteo, filtrado). Hay que decidir cómo llegan las respuestas a las reglas.

## Factores de decisión

- Casos de prueba independientes y repetibles.
- Cumplir el uso obligatorio de listas.
- Evitar limpiar estado entre consultas.
- Reglas legibles.

## Opciones consideradas

1. Lista `Var-Valor` pasada como argumento (`R`) a todos los predicados que la necesitan.
2. Hechos dinámicos `respuesta/2` con `assertz`/`retractall` por consulta.
3. Híbrido: Python hace `assert` de cada respuesta.

## Decisión

**Opción 1.** `respuesta(R, Var, Val) :- member(Var-Val, R).` es el único acceso a la lista; las reglas reciben `R` como primer argumento. Las reglas conservan el estilo del Entregable 1 (`respuesta(...)`), con un argumento más.

## Consecuencias

- **Positivas:** sin estado global; cada caso de prueba es una consulta pura; el requisito de listas se cumple de forma natural; no hay fugas entre consultas.
- **Negativas / deuda aceptada:** casi todos los predicados llevan `R`; las firmas son algo más largas.
- **Cuándo revisarla:** si se añade una sesión interactiva con memoria larga (fuera de alcance).

## Pros y contras de las opciones

### Hechos dinámicos

- ➕ Reglas más cortas.
- ➖ Estado global; olvidos de `retractall` contaminan las pruebas; Python tendría que hacer varios `assert` (más puente, más fallos).
