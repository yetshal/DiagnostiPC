# ADR-001: Prolog como única fuente de lógica; Python solo como puente

- **Estado:** Aceptada
- **Fecha:** 2026-10-21
- **Decisores:** Pareja (Líder de Conocimiento y Líder de Integración)
- **Tarea relacionada:** F0-02, F3-01

## Contexto y problema

Los requisitos de la asignatura exigen que toda la inferencia, el descarte, la validación de listas y el cálculo de severidad residan en Prolog, y que Python envíe datos, invoque predicados y presente resultados. Además, el Entregable 1 justificó el sistema experto por la **separación entre conocimiento y código**: agregar una falla debe requerir solo editar la base en Prolog.

## Factores de decisión

- Cumplir el requisito 3.4 (responsabilidad estricta de la lógica).
- Poder cambiar reglas sin tocar Python.
- Pruebas de la lógica sin depender de la consola ni del puente.
- Evitar duplicar el conocimiento en dos lenguajes.

## Opciones consideradas

1. Prolog contiene lógica, textos, catálogo de preguntas y orden de resultados; Python formatea y captura.
2. Prolog solo infiere; Python ordena, filtra y arma los textos.
3. Lógica repartida según comodidad.

## Decisión

**Opción 1.** Python no decide: no filtra, no ordena, no calcula certeza ni severidad y no contiene textos de dominio. El catálogo de preguntas (`pregunta/3`, `valor_permitido/2`) y las recomendaciones son hechos de Prolog que Python lee.

## Consecuencias

- **Positivas:** cumplimiento directo; la base se prueba con plunit sin Python; cambiar conocimiento no toca la interfaz.
- **Negativas / deuda aceptada:** algo de lógica "aburrida" (ordenar, formatear listas) se escribe en Prolog; el puente debe devolver estructuras planas.
- **Cuándo revisarla:** nunca durante el curso; es un requisito.

## Pros y contras de las opciones

### Opción 2

- ➕ Ordenar en Python es trivial.
- ➖ Incumple el requisito 3.4; el orden por prioridad es parte del razonamiento.

### Opción 3

- ➕ Ninguna real.
- ➖ Lógica duplicada y difícil de justificar en la sustentación.
