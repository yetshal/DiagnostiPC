# ADR-006: Interacción solo por consola (sin Tkinter)

- **Estado:** Aceptada
- **Fecha:** 2026-10-21
- **Decisores:** Pareja (confirmar con el docente en F0-04)
- **Tarea relacionada:** F3-02

## Contexto y problema

El Entregable 1 (objetivo específico 3) prometía una interfaz gráfica en Tkinter. Los requisitos técnicos posteriores indican explícitamente "sin interfaz gráfica; toda la interacción será por consola".

## Factores de decisión

- Cumplir los requisitos vigentes.
- Reducir riesgo y tiempo.
- Evitar lógica de presentación enredada con el puente.

## Opciones consideradas

1. Solo consola.
2. Consola + Tkinter opcional.
3. Solo Tkinter.

## Decisión

**Opción 1.** Los requisitos vigentes prevalecen sobre el Entregable 1. Se registra la discrepancia en `docs/ai/01 §6` y se pregunta al docente en F0-04 para confirmar que el cambio es aceptable.

## Consecuencias

- **Positivas:** menos código; más tiempo para la base de conocimiento, que es lo evaluado.
- **Negativas / deuda aceptada:** el objetivo 3 del Entregable 1 queda redactado de otra forma; se actualiza en la ficha final.
- **Cuándo revisarla:** si el docente pide GUI explícitamente.

## Pros y contras de las opciones

### Tkinter

- ➕ Más vistoso.
- ➖ Fuera de requisitos; riesgo de colar lógica en Python.
