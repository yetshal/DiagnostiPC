# docs/ai — Memoria del proyecto para agentes de IA

Esta carpeta guarda las reglas, el contexto y el estado del proyecto para que cualquier agente de IA pueda continuar el trabajo sin analizar todo el repositorio.

## Archivos

| Archivo                     | Para qué sirve                                                                                    | Quién lo lee                                 | Quién lo actualiza                           |
| --------------------------- | ------------------------------------------------------------------------------------------------- | -------------------------------------------- | -------------------------------------------- |
| `../../AGENTS.md`           | Punto de entrada: reglas de oro y protocolos de inicio/cierre                                     | Agente, siempre                              | Pareja                                       |
| `../../CLAUDE.md`           | Puente para Claude Code (importa AGENTS.md y el estado)                                           | Claude Code                                  | Pareja                                       |
| `01-contexto-proyecto.md`   | Producto, requisitos (MoSCoW), conciliación Entregable 1 ↔ requisitos                             | Agente, cuando necesita contexto             | Pareja                                       |
| `02-arquitectura.md`        | Fuente de verdad técnica: capas, secciones del `.pl`, contrato Python↔Prolog, certeza y severidad | Agente, al tocar lógica o puente             | Pareja (el agente propone)                   |
| `03-pautas-programacion.md` | Cómo escribir Prolog y Python, pruebas, git, DoD                                                  | Agente, al programar                         | Pareja                                       |
| `04-hoja-de-ruta.md`        | Plan por fases: tareas con AC, dependencias y responsable                                         | Agente: su tarea y su grupo de `§Pendientes` | Agente marca estados; pareja agrega tareas   |
| `05-estado-sesion.md`       | **Traspaso:** última sesión, tarea actual, qué leer                                               | Agente, **siempre** al iniciar               | Agente, **siempre** al cerrar (se reescribe) |
| `06-bitacora.md`            | Historial de sesiones, tiempos y correcciones humanas                                             | Pareja (el agente no lo lee)                 | Agente al cerrar (se agrega arriba)          |
| `07-decisiones.md`          | Índice de decisiones y su motivo                                                                  | Agente, por ID                               | Agente y pareja                              |
| `08-glosario.md`            | Variables, diagnósticos, escalas y términos (español ↔ código)                                    | Agente, al nombrar cosas                     | Agente y pareja                              |
| `09-guia-trabajo-con-ia.md` | Cómo trabajar en pareja con agentes y mantener el plazo                                           | Pareja                                       | Pareja                                       |
| `10-errores-conocidos.md`   | Trampas de Prolog, del puente y del proceso                                                       | Agente, al depurar: títulos y luego el ID    | Agente                                       |
| `templates/`                | Prompts de inicio, cierre y verificación; checklist; ficha de regla; ADR; tarea                   | Pareja y agente                              | Pareja                                       |

## Orden de lectura del agente al iniciar

`AGENTS.md` → `05-estado-sesion.md` → archivos que indique el estado → (según la tarea, solo la sección o el ID) `02`, `03`, `04`, `08`, `07`, `10`. `06` y `docs/product/` no se leen salvo que la tarea trate de ellos (las tareas de conocimiento sí leen `docs/product/adquisicion-conocimiento.md`).
