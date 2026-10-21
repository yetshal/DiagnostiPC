# Prompt de cierre de sesión

```text
Cierra la sesión siguiendo `AGENTS.md §5`:

1. Ejecuta `swipl -q -g run_tests -t halt tests/tests_kb.pl` y, si tocaste la frontera, `python pruebas.py`. Pega la salida real y resumida, incluyendo advertencias de carga.
2. Actualiza `docs/ai/04-hoja-de-ruta.md`: estado de la tarea (`[x]`, `[~]` o `[!]` con motivo) y los pendientes descubiertos en su grupo, cada uno con tu recomendación.
3. REESCRIBE completo `docs/ai/05-estado-sesion.md` con su estructura.
4. AGREGA arriba una entrada en `docs/ai/06-bitacora.md` (máx. 10 líneas, incluye tiempo estimado y correcciones humanas).
5. Registra decisiones en `07-decisiones.md`, términos nuevos en `08` y errores no obvios en `10`. Si cambió un predicado público, actualiza `docs/entregables/03-diccionario-predicados.md`.
6. Termina con un INFORME FINAL:
   - Estado: qué quedó hecho y qué no.
   - Pruebas: comandos y resultados.
   - Reglas nuevas: lista con su fuente o `[PENDIENTE-VALIDAR]` (para llevarlas al técnico).
   - Pendientes: cada uno con tu recomendación (hacerlo ahora / en qué tarea / no hacerlo).
   - Commit: mensaje convencional listo para copiar y rama.
   - Lo que nos toca a nosotros (revisión cruzada, PR, preguntas al docente o al técnico).
```
