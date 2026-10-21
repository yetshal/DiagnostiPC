# docs/ai — Memoria del proyecto para agentes de IA

Esta carpeta guarda las reglas, el contexto y el estado del proyecto para que cualquier agente de IA pueda continuar el trabajo sin sobrecargar el contexto.

## Archivos de Memoria y Control

| Archivo                     | Para qué sirve                                                                           | Quién lo lee                      | Quién lo actualiza                           |
| --------------------------- | ---------------------------------------------------------------------------------------- | --------------------------------- | -------------------------------------------- |
| `../../AGENTS.md`           | Punto de entrada: reglas de oro y protocolos de inicio/cierre                            | Agente, siempre                   | Pareja                                       |
| `../../CLAUDE.md`           | Puente para Claude Code (importa `AGENTS.md` y el estado)                                | Claude Code                       | Pareja                                       |
| `01-contexto-proyecto.md`   | Contexto general, requisitos del curso y conciliación Entregable 1                       | Agente, cuando necesita contexto  | Pareja                                       |
| `02-arquitectura.md`        | Fuente de verdad técnica: capas, secciones del `.pl`, contrato Python↔Prolog y severidad | Agente, al tocar lógica o puente  | Pareja (el agente propone)                   |
| `03-pautas-programacion.md` | Pautas de código Prolog y Python, pruebas, git y DoD                                     | Agente, al programar              | Pareja                                       |
| `04-hoja-de-ruta.md`        | Plan por fases: tareas con criterios de aceptación y dependencias                        | Agente: tarea actual y pendientes | Agente marca estados; pareja agrega tareas   |
| `05-estado-sesion.md`       | **Traspaso:** última sesión, estado actual, tareas concluidas y verificación             | Agente, **siempre** al iniciar    | Agente, **siempre** al cerrar (se reescribe) |
| `06-bitacora.md`            | Historial de sesiones, tiempos y correcciones                                            | Pareja                            | Agente al cerrar (se agrega arriba)          |
| `07-decisiones.md`          | Índice de decisiones técnicas y su justificación                                         | Agente, por ID                    | Agente y pareja                              |
| `08-glosario.md`            | Síntomas, diagnósticos, escalas y componentes (español ↔ código)                         | Agente, al nombrar entidades      | Agente y pareja                              |
| `09-guia-trabajo-con-ia.md` | Metodología de trabajo en pareja con agentes de IA                                       | Pareja                            | Pareja                                       |
| `10-errores-conocidos.md`   | Trampas comunes de Prolog, PySwip y del proceso                                          | Agente, al depurar                | Agente                                       |
| `templates/`                | Plantillas de inicio, cierre, verificación, fichas de regla y ADR                        | Pareja y agente                   | Pareja                                       |

## Orden de Lectura del Agente al Iniciar

`AGENTS.md` → `05-estado-sesion.md` → archivos indicados en el estado de traspaso.
