# ADR-004: Encadenamiento lógico en tres niveles

- **Estado:** Aceptada
- **Fecha:** 2026-10-21
- **Decisores:** Pareja
- **Tarea relacionada:** F2-02, F2-03, F2-04…F2-06

## Contexto y problema

Los requisitos exigen reglas que dependan de otras reglas (no solo de hechos base) con tres niveles: validación preliminar, inferencia intermedia y conclusión final. El Entregable 1 ya planteaba "síntomas → categoría → diagnóstico".

## Factores de decisión

- Cumplimiento verificable del requisito 3.1.
- Reglas pequeñas y probables una por una.
- Evitar ciclos.

## Opciones consideradas

1. N1 condiciones elementales sobre la lista; N2 categorías e indicios (usan N1); N3 diagnósticos (usan N2 y N1).
2. Un solo nivel de reglas grandes que consultan la lista.
3. Niveles dinámicos con meta-intérprete.

## Decisión

**Opción 1**, con dependencia **estrictamente descendente**: N3 → N2 → N1 → hechos. Ningún predicado de un nivel llama a uno de nivel superior, lo que elimina ciclos por construcción. Los predicados se agrupan en secciones del `.pl` con el nivel en el encabezado, y cada diagnóstico (N3) cita en su comentario la categoría (N2) de la que depende.

## Consecuencias

- **Positivas:** el grafo de dependencias es un árbol (se dibuja en `docs/architecture`); cada nivel se prueba por separado.
- **Negativas / deuda aceptada:** más predicados pequeños; hay que resistir la tentación de "saltarse" un nivel.
- **Cuándo revisarla:** no aplica.

## Pros y contras de las opciones

### Meta-intérprete

- ➕ Permite explicaciones automáticas.
- ➖ Complejidad innecesaria; la explicación se resuelve con identificadores de regla.
