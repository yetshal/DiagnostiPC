# Prompt de inicio de sesión

Pega esto al abrir una sesión nueva (con Claude Code basta con "inicia la sesión"):

```text
Inicia la sesión de trabajo en DiagnostiPC.

1. Lee `AGENTS.md` y `docs/ai/05-estado-sesion.md`.
2. Lee solo lo que el estado indique como lectura obligatoria.
3. Resume en máximo 8 líneas: tarea actual, su AC, dependencias cumplidas y riesgos.
4. Presenta tu plan: predicados o archivos a crear/modificar, pruebas plunit a escribir primero y comandos a ejecutar.
5. Indica qué conocimiento técnico necesitas que no esté en las fuentes (para no inventarlo).
6. NO escribas código hasta que yo confirme el plan.
```

## Variante: tarea distinta a la del estado

```text
Inicia la sesión de trabajo en DiagnostiPC, pero la tarea de hoy es <ID> (no la de `05`).
Lee `AGENTS.md`, `05-estado-sesion.md` y la línea de <ID> en `04-hoja-de-ruta.md` con sus dependencias.
Si alguna dependencia no está en [x], dímelo antes de planear.
Presenta el plan y espera mi confirmación.
```
