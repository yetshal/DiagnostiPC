# Producto — alcance, cronograma y riesgos

> Versión corta para decisiones de alcance. Requisitos completos: `docs/ai/01-contexto-proyecto.md`.

## Problema y propuesta de valor

> «Dime qué observas en tu computador y te digo qué le pasa probablemente, qué tan urgente es y qué hacer primero.»

## Alcance

**Sí:** 38 variables de entrada, 10 diagnósticos, tres niveles de reglas, certeza, severidad ajustada, recolección ordenada, consola, pruebas.
**No:** interfaz gráfica, servidores, Mac, periféricos, fallas de red, recuperación de datos.

## Cronograma por fases (en sesiones; fechas por definir)

| Fase                     | Sesiones | Hito                                                                |
| ------------------------ | -------- | ------------------------------------------------------------------- |
| F0 Preparación           | S1–S2    | Puente probado y plunit corriendo; dudas con el docente resueltas   |
| F1 Conocimiento y hechos | S3–S5    | Catálogos, tabla de conocimiento validada, validación de listas     |
| F2 Motor lógico          | S6–S10   | N1–N3, certeza, severidad, recolección; **decisión de recorte**     |
| F3 Integración           | S11–S13  | `motor_inferencia.py`, `main.py`, `pruebas.py`                      |
| F4 Entrega               | S14–S15  | Diccionario, evidencia, ficha, matriz 100 %, ensayo de sustentación |

Para convertirlo a fechas: sesión S1 = día de inicio; con una sesión diaria, S15 ≈ día 15; deja 2 días de colchón antes de la entrega.

## Riesgos principales

| Riesgo                                                         | Prob. | Impacto | Mitigación                                                                           |
| -------------------------------------------------------------- | ----- | ------- | ------------------------------------------------------------------------------------ |
| El puente (PySwip/Janus) no funciona en alguna máquina         | Media | Alto    | Spike en F0-02; puente aislado (ADR-002); probar en ambas máquinas                   |
| Reglas con conocimiento técnico incorrecto                     | Alta  | Alto    | Fuentes obligatorias; dos reuniones con el técnico; marca `[PENDIENTE-VALIDAR]`      |
| La IA mete lógica en Python o reglas que se saltan niveles     | Media | Alto    | `AGENTS.md`; checklist; verificación de F2-10 y F4-05                                |
| Ciclos o cortes mal puestos que dan resultados inestables      | Media | Medio   | Dependencias descendentes; pruebas con entradas aleatorias; comentarios obligatorios |
| Discrepancia Entregable 1 ↔ requisitos (Tkinter, nº de reglas) | Alta  | Medio   | Conciliación en `01 §6`; preguntas al docente en F0-04                               |
| Se concentra el conocimiento en una persona                    | Media | Medio   | Revisión cruzada de cada PR; ensayo de sustentación mutuo                            |
| Retraso acumulado                                              | Media | Alto    | Regla de recorte fija (`04`)                                                         |
| Problemas de codificación (tildes) en Windows                  | Media | Bajo    | Identificadores sin tildes; prueba en F0-02                                          |

## Qué NO prometer

No es un sustituto del técnico: diagnostica causas **probables** a partir de lo que el usuario reporta, no mide el hardware. Cuando la evidencia no alcanza, el sistema lo dice.
